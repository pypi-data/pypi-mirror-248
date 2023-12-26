import base64
import ddddocr


class CharVerifyCodeOcr:
    
    @classmethod
    def ocr_from_b64(self, b64):
        """从base64图片中识别"""
        
        ocr = ddddocr.DdddOcr(show_ad=False)
        return ocr.classification(base64.b64decode(b64))
