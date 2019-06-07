USING_HTTPS = True

# Use JSCover
MUST_FS_COVER = False # If this is set true, error will be raised when we cannot detect jscover's instrumented code
COVERAGE_DIR = "test/coverage/front/" # The temp dir for jscover's unmerged coverage file

# We use Fiddler as our proxy, which is conflict with using JSCover as the proxy.
# So unless we can set two levels of proxy, we will never be able to use JSCover's proxy service.
PROXY_COVER = False 