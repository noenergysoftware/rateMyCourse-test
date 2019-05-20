USING_HTTPS = True

# Use JSCover
FS_COVER = True

# We use Fiddler as our proxy, which is conflict with using JSCover as the proxy.
# So unless we can set two levels of proxy, we will never be able to use JSCover's proxy service.
PROXY_COVER = False 