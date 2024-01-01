import numpy as np
import cv2
from . import ebsynth as eb

class Imagesynth:
    INVALID_STYLE_IMG = 'style_img must be a str leading to a valid file path or a 3-channel numpy array'
    INVALID_GUIDE_FORMAT = 'guides must be a list of lists in the format [guide 1, guide 2, weight]'
    INVALID_OUTPUT_PATH = 'output_path must be a str leading to a valid file path or None'
    def __init__(self, style_img):
        """
        Initialize the ebsynth object.
        
        Parameters
        ----------
        style_img: str or numpy array
        >>> str leading to file path, or numpy array
        
        guides: tuple of lists
        >>> [[guide 1, guide 2, weight], [guide 1, guide 2, weight], ...]
        >>> guide 1: str leading to file path, or numpy array
        >>> guide 2: str leading to file path, or numpy array
        >>> weight: float
        
        Example
        -------
        from ezsynth import imagesynth
        
        >>> STYLE_PATH = "Style.jpg" or np.array
        >>> SOURCE_IMG = "Source.jpg" or np.array
        >>> TARGET_IMG = "Target.jpg" or np.array
        >>> OUTPUT_PATH = "Output.jpg" or None
        
        >>> eb = imagesynth(style_img = STYLE_PATH)
        >>> eb.add_guide(source = SOURCE_IMG, target = TARGET_IMG, weight = 1.0)
        >>> eb.run(output_path = OUTPUT_PATH)
        >>> or to do something else result = eb.run()
        
        """
        self.style_img = self._validate_style_img(style_img)
        self.device = 'cuda'
        self.eb = eb.Ebsynth(style = style_img, guides = [])
    
    def add_guide(self, source, target, weight):
        """
        Add a guide to the ebsynth object.
        
        Parameters
        ----------
        source: str or numpy array
        >>> str leading to file path, or numpy array
        
        target: str or numpy array
        >>> str leading to file path, or numpy array
        
        weight: float
        """
        
        self._validate_guide([source, target, weight])
        self.eb.add_guide(source, target, weight)
        
    def clear_guides(self):
        self.eb.clear_guides()
    
    @staticmethod
    def _validate_image(img):
        if isinstance(img, str):
            img = cv2.imread(img)
            if img is None:
                raise ValueError(Imagesynth.INVALID_STYLE_IMG)
        elif isinstance(img, np.ndarray):
            if img.shape[-1] != 3:
                raise ValueError(Imagesynth.INVALID_STYLE_IMG)
        else:
            raise ValueError(Imagesynth.INVALID_STYLE_IMG)
        return img
    
    def _validate_style_img(self, style_img):
        return self._validate_image(style_img)
    
    def _validate_guide(self, guide):
        if len(guide) != 3:
            raise ValueError(Imagesynth.INVALID_GUIDE_FORMAT)
        self._validate_image(guide[0])
        self._validate_image(guide[1])
        if not isinstance(guide[2], float):
            raise ValueError('weight must be a float')
        
    def _validate_output_path(self, output_path):
        if not (isinstance(output_path, str) or output_path is None):
            raise ValueError(Imagesynth.INVALID_OUTPUT_PATH)
        return output_path

    def run(self, output_path = None):
        """
        Run ebsynth.
        
        Parameters
        ----------
        output_path: str(optional)
        >>> str leading to file path
        
        returns: numpy array
        
        """
        output_path = self._validate_output_path(output_path)
        result, _ = self.eb.run(output_nnf = True)

        if output_path:
            cv2.imwrite(output_path, result)
            
        return result

