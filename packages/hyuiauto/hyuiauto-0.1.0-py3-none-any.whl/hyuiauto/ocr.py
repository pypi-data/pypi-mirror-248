# import pprint



class OCR:              

    def imgToText(self, screen:bytes) -> str:        
        pass
           

    def imgToTexts(self, screen:bytes)-> list[str]:   
        pass




class OCR_Paddle(OCR):
    
    def __init__(self, **kargs):
        from paddleocr import PaddleOCR
        self.ocrEngine = PaddleOCR(lang='ch' , 
                 use_angle_cls=False, 
                 enable_mkldnn=True,
                 show_log=False, 
                 det_db_box_thresh=0.80,
                 **kargs
                 ) 
        

    def imgToText(self, screen:bytes)-> str:    
        
        ret =  self.ocrEngine.ocr(screen,  cls=False)

        lines = ret[0]

        # pprint.pprint(lines,indent=2)
        # print('\n\n')

        if not lines:
            return ''
        
        ret = [line[1][0] for line in lines]

        return '\n'.join(ret)
            

    def imgToTexts(self, screen:bytes)-> list[str]:   
        ret = self.ocrEngine.ocr(screen,  cls=False)

        lines = ret[0]

        if not lines:
            return []
        
        return lines

class CFG:
    Default_OCR = OCR_Paddle