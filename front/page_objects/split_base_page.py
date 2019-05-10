from .basic_page import BasicPage
from functools import wraps

class SplitBasePage(BasicPage):
    def __init__(
        self, 
        driver,
        url,
        prev_btn_loc,
        next_btn_loc,
        jump_text_loc,
        jump_btn_loc,
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
        self.jump_text_loc      = jump_text_loc
        self.jump_btn_loc       = jump_btn_loc
        self.now_index_text_loc = now_index_text_loc
        self.max_index_text_loc = max_index_text_loc
        self.block_div_loc      = block_div_loc
        self.block_relative_loc = block_relative_loc
        self.form_get_method    = form_get_method

        self.block_cache = None


    def splitChanged(f):
        @wraps(f)
        def wrap_func(self):
            self.block_cache = None
            return f(self)
        return wrap_func

    def getBlocks(self):
        if self.block_cache == None:
            block_div = self.waitAppear(self.block_div_loc)
            self.block_cache = block_div.find_elements(*self.block_relative_loc)
        return self.block_cache

    def getBlockNum(self):
        return len(self.getBlocks())

    def getBlockForm(self, index):
        if index >= self.getBlockNum():
            raise Exception("Index {0} is too large.".format(index))
        block = self.getBlocks()[index]
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
        text = self.waitAppear(self.jump_text_loc)
        text.send_keys(str(index))
        btn = self.waitAppear(self.jump_btn_loc)
        btn.click()

    def getNowIndex(self):
        return int(self.waitAppear(self.now_index_text_loc).text)

    def getMaxIndex(self):
        return int(self.waitAppear(self.max_index_text_loc).text)