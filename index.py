import logging as log
log.basicConfig(level=log.NOTSET)  # 设置日志级别

def err_default(step):
    log.info("something bad in step:"+str(step))


def fcb_default(step):
    log.info("done after: "+str(step)+"step")


class PipWorkUnit:
    def __init__(self, fto, ferr = err_default, fcb = fcb_default):
        self.step = 0
        self.status = True
        self.fto = fto
        self.ferr = ferr
        self.fcb = fcb
    
    def start(self):
        if not self.status:
            return self
        try:
            self.fto()
        except Exception as e:
            self.status = False
            log.info(e)
            self.ferr(int(self.step))
            # sys.exit()
        finally:
            self.fcb(self.step)
            return self

    def then(self, fto, ferr = err_default, fcb = fcb_default):
        if not self.status:
            return self
        self.step += 1
        self.fto = fto
        self.ferr = ferr
        self.fcb = fcb
        return self

    def done(self):
        try:
            self.fto()
        except Exception as e:
            log.info("error:",e)
            self.ferr(self.step)
            self.status = False
        finally:
            self.fcb(self.step)