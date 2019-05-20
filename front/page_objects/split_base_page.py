from .basic_page import BasicPage
from functools import wraps
from test.front.util import rs

import copy

class SplitBasePage(BasicPage):
    def __init__(
        self, 
        driver,
        url,
        prev_btn_loc,
        next_btn_loc,
        # jump_text_loc,
        # jump_btn_loc,
        split_btn_loc_temp,
        split_btn_div_loc,
        prev_dot_loc,
        next_dot_loc,
        now_index_text_loc,
        max_index_text_loc,
        block_div_loc,
        block_relative_loc,
        form_get_method,
        ):
        super().__init__(driver, url)

        self.driver             = driver
        self.prev_btn_loc       = prev_btn_loc
        self.next_btn_loc       = next_btn_loc
        # self.jump_text_loc      = jump_text_loc
        # self.jump_btn_loc       = jump_btn_loc
        self.split_btn_loc_temp = split_btn_loc_temp
        self.split_btn_div_loc  = split_btn_div_loc
        self.prev_dot_loc       = prev_dot_loc
        self.next_dot_loc       = next_dot_loc
        self.now_index_text_loc = now_index_text_loc
        self.max_index_text_loc = max_index_text_loc
        self.block_div_loc      = block_div_loc
        self.block_relative_loc = block_relative_loc
        self.form_get_method    = form_get_method

        self.block_cache = None
        self.now_index = 1


    def splitChanged(f):
        @wraps(f)
        def wrap_func(self, *args, **kwargs):
            self.block_cache = None

            res = f(self, *args, *kwargs)

            def func_comp(a, b):
                return a.__name__ == b.__name__

            if func_comp(f, SplitBasePage.prevSplit):
                self.now_index -= 1
            elif func_comp(f, SplitBasePage.nextSplit):
                self.now_index += 1
            elif func_comp(f, SplitBasePage.jumpSplit):
                self.now_index = args[0]

            rs()
            return res
        return wrap_func

    def getBlocks(self):
        if self.block_cache == None:
            block_div = self.waitAppear(self.block_div_loc)
            self.block_cache = block_div.find_elements(*self.block_relative_loc)
        return self.block_cache

    def getBlock(self, index):
        if index >= self.getBlockNum():
            raise Exception("Index {0} is too large.".format(index))
        return self.getBlocks()[index]

    def getBlockNum(self):
        return len(self.getBlocks())

    def getBlockForm(self, index):
        block = self.getBlock(index)
        return self.form_get_method(block)

    @splitChanged
    def prevSplit(self):
        btn = self.waitAppear(self.prev_btn_loc)
        btn.click()

    @splitChanged
    def nextSplit(self):
        btn = self.waitAppear(self.next_btn_loc)
        btn.click()

    @splitChanged
    def jumpSplit(self, index):
        ''' Note: The split btn must be shown.
        '''
        btn = self._getSplitBtn(index)
        btn.click()
        # text = self.waitAppear(self.jump_text_loc)
        # text.send_keys(str(index))
        # btn = self.waitAppear(self.jump_btn_loc)
        # btn.click()

    def getNowIndex(self):
        return self.now_index
        # return int(self.waitAppear(self.now_index_text_loc).text)

    def getMaxIndex(self):
        div = self.waitAppear(self.split_btn_div_loc)
        btn_list = div.find_elements_by_xpath("./*")

        return len(btn_list) - 4
        # return int(self.waitAppear(self.max_index_text_loc).text)

    def _checkShow(self, ctl):
        style = ctl.get_attribute("style")
        if "none" in style:
            return False
        else:
            return True

    def _getSplitBtn(self, index):
        loc = copy.deepcopy(self.split_btn_loc_temp)
        return self.waitPresence((loc[0], loc[1].format(index)))

    def checkBtnShow(self):
        now_index = self.getNowIndex()
        max_index = self.getMaxIndex()

        # Check next and prev btn
        if max_index >= 2:
            prev_btn = self.waitPresence(self.prev_btn_loc)
            next_btn = self.waitPresence(self.next_btn_loc)

            if now_index != 1:
                assert(self._checkShow(prev_btn))
            else:
                assert(not self._checkShow(prev_btn))

            if now_index != max_index:
                assert(self._checkShow(next_btn))
            else:
                assert(not self._checkShow(next_btn))

        # Check split btn and dot
        btns = [None]
        for i in range(1, max_index+1):
            btns.append(self._getSplitBtn(i))
        prev_dot = self.waitPresence(self.prev_dot_loc)
        next_dot = self.waitPresence(self.next_dot_loc)

        # First and last btn should always show
        assert(self._checkShow(btns[1]))
        assert(self._checkShow(btns[max_index]))

        if now_index <= 4:
            if max_index <= 6:
                # btn all show and no dot
                for i in range(1, max_index+1):
                    assert(self._checkShow(btns[i]))
                assert(not self._checkShow(prev_dot))
                assert(not self._checkShow(next_dot))
            else:
                # only show [1, 5] and the last btn
                # no prev_dot, has next_dot
                for i in range(1, 5+1):
                    assert(self._checkShow(btns[i]))
                for i in range(6, max_index):
                    assert(not self._checkShow(btns[i]))

                assert(not self._checkShow(prev_dot))
                assert(self._checkShow(next_dot))
        elif now_index >= max_index -3:
            if max_index <= 6:
                # btn all show and no dot
                for i in range(1, max_index+1):
                    assert(self._checkShow(btns[i]))
            else:
                # only show [last-4, last] and the first btn
                # has prev_dot, no next_dot
                for i in range(max_index-4, max_index+1):
                    assert(self._checkShow(btns[i]))
                for i in range(2, max_index-4):
                    assert(not self._checkShow(btns[i]))

                assert(self._checkShow(prev_dot))
                assert(not self._checkShow(next_dot))
        else:
            # only show [now-2, now+2] and the first, last btn
            # has prev_dot, has next_dot
            for i in range(now_index-2, now_index+3):
                assert(self._checkShow(btns[i]))
            for i in range(2, now_index-2):
                assert(not self._checkShow(btns[i]))
            for i in range(now_index+3, max_index):
                assert(not self._checkShow(btns[i]))
            assert(self._checkShow(prev_dot))
            assert(self._checkShow(next_dot))


        


