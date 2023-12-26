"""The namespace handles Filter options."""
from typing import List, Optional, Dict, Iterable
import enum
import aspose.pycore
import aspose.pydrawing
import aspose.imaging
import aspose.imaging.apsbuilder
import aspose.imaging.apsbuilder.dib
import aspose.imaging.asynctask
import aspose.imaging.brushes
import aspose.imaging.dithering
import aspose.imaging.exif
import aspose.imaging.exif.enums
import aspose.imaging.extensions
import aspose.imaging.fileformats
import aspose.imaging.fileformats.apng
import aspose.imaging.fileformats.bigtiff
import aspose.imaging.fileformats.bmp
import aspose.imaging.fileformats.bmp.structures
import aspose.imaging.fileformats.cdr
import aspose.imaging.fileformats.cdr.const
import aspose.imaging.fileformats.cdr.enum
import aspose.imaging.fileformats.cdr.objects
import aspose.imaging.fileformats.cdr.types
import aspose.imaging.fileformats.cmx
import aspose.imaging.fileformats.cmx.objectmodel
import aspose.imaging.fileformats.cmx.objectmodel.enums
import aspose.imaging.fileformats.cmx.objectmodel.specs
import aspose.imaging.fileformats.cmx.objectmodel.styles
import aspose.imaging.fileformats.core
import aspose.imaging.fileformats.core.vectorpaths
import aspose.imaging.fileformats.dicom
import aspose.imaging.fileformats.djvu
import aspose.imaging.fileformats.dng
import aspose.imaging.fileformats.dng.decoder
import aspose.imaging.fileformats.emf
import aspose.imaging.fileformats.emf.dtyp
import aspose.imaging.fileformats.emf.dtyp.commondatastructures
import aspose.imaging.fileformats.emf.emf
import aspose.imaging.fileformats.emf.emf.consts
import aspose.imaging.fileformats.emf.emf.objects
import aspose.imaging.fileformats.emf.emf.records
import aspose.imaging.fileformats.emf.emfplus
import aspose.imaging.fileformats.emf.emfplus.consts
import aspose.imaging.fileformats.emf.emfplus.objects
import aspose.imaging.fileformats.emf.emfplus.records
import aspose.imaging.fileformats.emf.emfspool
import aspose.imaging.fileformats.emf.emfspool.records
import aspose.imaging.fileformats.emf.graphics
import aspose.imaging.fileformats.eps
import aspose.imaging.fileformats.eps.consts
import aspose.imaging.fileformats.gif
import aspose.imaging.fileformats.gif.blocks
import aspose.imaging.fileformats.ico
import aspose.imaging.fileformats.jpeg
import aspose.imaging.fileformats.jpeg2000
import aspose.imaging.fileformats.opendocument
import aspose.imaging.fileformats.opendocument.enums
import aspose.imaging.fileformats.opendocument.objects
import aspose.imaging.fileformats.opendocument.objects.brush
import aspose.imaging.fileformats.opendocument.objects.font
import aspose.imaging.fileformats.opendocument.objects.graphic
import aspose.imaging.fileformats.opendocument.objects.pen
import aspose.imaging.fileformats.pdf
import aspose.imaging.fileformats.png
import aspose.imaging.fileformats.psd
import aspose.imaging.fileformats.svg
import aspose.imaging.fileformats.svg.graphics
import aspose.imaging.fileformats.tga
import aspose.imaging.fileformats.tiff
import aspose.imaging.fileformats.tiff.enums
import aspose.imaging.fileformats.tiff.filemanagement
import aspose.imaging.fileformats.tiff.filemanagement.bigtiff
import aspose.imaging.fileformats.tiff.instancefactory
import aspose.imaging.fileformats.tiff.pathresources
import aspose.imaging.fileformats.tiff.tifftagtypes
import aspose.imaging.fileformats.webp
import aspose.imaging.fileformats.wmf
import aspose.imaging.fileformats.wmf.consts
import aspose.imaging.fileformats.wmf.graphics
import aspose.imaging.fileformats.wmf.objects
import aspose.imaging.fileformats.wmf.objects.escaperecords
import aspose.imaging.imagefilters
import aspose.imaging.imagefilters.filteroptions
import aspose.imaging.imageloadoptions
import aspose.imaging.imageoptions
import aspose.imaging.interfaces
import aspose.imaging.magicwand
import aspose.imaging.magicwand.imagemasks
import aspose.imaging.masking
import aspose.imaging.masking.options
import aspose.imaging.masking.result
import aspose.imaging.memorymanagement
import aspose.imaging.multithreading
import aspose.imaging.palettehelper
import aspose.imaging.progressmanagement
import aspose.imaging.shapes
import aspose.imaging.shapesegments
import aspose.imaging.sources
import aspose.imaging.watermark
import aspose.imaging.watermark.options
import aspose.imaging.xmp
import aspose.imaging.xmp.schemas
import aspose.imaging.xmp.schemas.dicom
import aspose.imaging.xmp.schemas.dublincore
import aspose.imaging.xmp.schemas.pdf
import aspose.imaging.xmp.schemas.photoshop
import aspose.imaging.xmp.schemas.xmpbaseschema
import aspose.imaging.xmp.schemas.xmpdm
import aspose.imaging.xmp.schemas.xmpmm
import aspose.imaging.xmp.schemas.xmprm
import aspose.imaging.xmp.types
import aspose.imaging.xmp.types.basic
import aspose.imaging.xmp.types.complex
import aspose.imaging.xmp.types.complex.colorant
import aspose.imaging.xmp.types.complex.dimensions
import aspose.imaging.xmp.types.complex.font
import aspose.imaging.xmp.types.complex.resourceevent
import aspose.imaging.xmp.types.complex.resourceref
import aspose.imaging.xmp.types.complex.thumbnail
import aspose.imaging.xmp.types.complex.version
import aspose.imaging.xmp.types.derived

class BigRectangularFilterOptions(FilterOptionsBase):
    '''Big Rectangular Filter Options'''
    
    def __init__(self):
        ...
    
    ...

class BilateralSmoothingFilterOptions(FilterOptionsBase):
    '''The Bilateral Smoothing Filter Options.'''
    
    @overload
    def __init__(self, size: int):
        '''Initializes a new instance of the  class.
        
        :param size: Size of the kernal.'''
        ...
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @property
    def size(self) -> int:
        '''Gets the size of the kernel.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Sets the size of the kernel.'''
        ...
    
    @property
    def spatial_factor(self) -> float:
        ...
    
    @spatial_factor.setter
    def spatial_factor(self, value : float):
        ...
    
    @property
    def spatial_power(self) -> float:
        ...
    
    @spatial_power.setter
    def spatial_power(self, value : float):
        ...
    
    @property
    def color_factor(self) -> float:
        ...
    
    @color_factor.setter
    def color_factor(self, value : float):
        ...
    
    @property
    def color_power(self) -> float:
        ...
    
    @color_power.setter
    def color_power(self, value : float):
        ...
    
    ...

class ConvolutionFilterOptions(FilterOptionsBase):
    '''The convolution filter.'''
    
    @property
    def factor(self) -> float:
        '''Gets the factor.'''
        ...
    
    @factor.setter
    def factor(self, value : float):
        '''Sets the factor.'''
        ...
    
    @property
    def bias(self) -> int:
        '''Gets the bias.'''
        ...
    
    @bias.setter
    def bias(self, value : int):
        '''Sets the bias.'''
        ...
    
    ...

class DeconvolutionFilterOptions(FilterOptionsBase):
    '''Deconvolution Filter Options, abstract class'''
    
    @property
    def snr(self) -> float:
        '''Gets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @snr.setter
    def snr(self, value : float):
        '''Sets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @property
    def brightness(self) -> float:
        '''Gets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @brightness.setter
    def brightness(self, value : float):
        '''Sets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @property
    def grayscale(self) -> bool:
        '''Gets a value indicating whether this  is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @grayscale.setter
    def grayscale(self, value : bool):
        '''Sets a value indicating whether this  is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @property
    def is_partial_loaded(self) -> bool:
        ...
    
    ...

class FilterOptionsBase:
    '''Filter Options Base, abstract class'''
    
    ...

class GaussWienerFilterOptions(DeconvolutionFilterOptions):
    '''Gauss Wiener Filter Options
    Deblur gauss'''
    
    @overload
    def __init__(self, radius: int, smooth: float):
        '''Initializes a new instance of the  class.
        
        :param radius: The radius.
        :param smooth: The smooth.'''
        ...
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.
        With default settings.'''
        ...
    
    @property
    def snr(self) -> float:
        '''Gets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @snr.setter
    def snr(self, value : float):
        '''Sets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @property
    def brightness(self) -> float:
        '''Gets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @brightness.setter
    def brightness(self, value : float):
        '''Sets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @property
    def grayscale(self) -> bool:
        '''Gets a value indicating whether this  is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @grayscale.setter
    def grayscale(self, value : bool):
        '''Sets a value indicating whether this  is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @property
    def is_partial_loaded(self) -> bool:
        ...
    
    @property
    def radius(self) -> int:
        '''Gets the radius.'''
        ...
    
    @radius.setter
    def radius(self, value : int):
        '''Sets the radius.'''
        ...
    
    @property
    def smooth(self) -> float:
        '''Gets the smooth.'''
        ...
    
    @smooth.setter
    def smooth(self, value : float):
        '''Sets the smooth.'''
        ...
    
    ...

class GaussianBlurFilterOptions(ConvolutionFilterOptions):
    '''The Gaussian blur'''
    
    @overload
    def __init__(self, radius: int, sigma: float):
        '''Initializes a new instance of the  class.
        
        :param radius: The radius.
        :param sigma: The sigma.'''
        ...
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.
        With default settings.'''
        ...
    
    @property
    def factor(self) -> float:
        '''Gets the factor.'''
        ...
    
    @factor.setter
    def factor(self, value : float):
        '''Sets the factor.'''
        ...
    
    @property
    def bias(self) -> int:
        '''Gets the bias.'''
        ...
    
    @bias.setter
    def bias(self, value : int):
        '''Sets the bias.'''
        ...
    
    @property
    def radius(self) -> int:
        '''Gets the radius.'''
        ...
    
    @radius.setter
    def radius(self, value : int):
        '''Sets the radius.'''
        ...
    
    @property
    def sigma(self) -> float:
        '''Gets the sigma.'''
        ...
    
    @sigma.setter
    def sigma(self, value : float):
        '''Sets the sigma.'''
        ...
    
    ...

class MedianFilterOptions(FilterOptionsBase):
    '''Median filter'''
    
    def __init__(self, size: int):
        '''Initializes a new instance of the  class.
        
        :param size: The size of filter rectangle.'''
        ...
    
    @property
    def size(self) -> int:
        '''Gets the size.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Sets the size.'''
        ...
    
    ...

class MotionWienerFilterOptions(DeconvolutionFilterOptions):
    '''Deconvolution filter options
    deblur motion'''
    
    def __init__(self, length: int, smooth: float, angle: float):
        '''Initializes a new instance of the  class.
        
        :param length: The length.
        :param smooth: The smooth.
        :param angle: The angle in gradus.'''
        ...
    
    @property
    def snr(self) -> float:
        '''Gets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @snr.setter
    def snr(self, value : float):
        '''Sets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @property
    def brightness(self) -> float:
        '''Gets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @brightness.setter
    def brightness(self, value : float):
        '''Sets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @property
    def grayscale(self) -> bool:
        '''Gets a value indicating whether this  is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @grayscale.setter
    def grayscale(self, value : bool):
        '''Sets a value indicating whether this  is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @property
    def is_partial_loaded(self) -> bool:
        ...
    
    @property
    def length(self) -> int:
        '''Gets the length.'''
        ...
    
    @length.setter
    def length(self, value : int):
        '''Sets the length.'''
        ...
    
    @property
    def smooth(self) -> float:
        '''Gets the smooth.'''
        ...
    
    @smooth.setter
    def smooth(self, value : float):
        '''Sets the smooth.'''
        ...
    
    @property
    def angle(self) -> float:
        '''Gets the angle in gradus.'''
        ...
    
    @angle.setter
    def angle(self, value : float):
        '''Sets the angle in gradus.'''
        ...
    
    ...

class SharpenFilterOptions(ConvolutionFilterOptions):
    '''The Sharpen filter options'''
    
    @overload
    def __init__(self, size: int, sigma: float):
        '''Initializes a new instance of the  class.
        
        :param size: Size of the kernel.
        :param sigma: The sigma.'''
        ...
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.
        With default settings.'''
        ...
    
    @property
    def factor(self) -> float:
        '''Gets the factor.'''
        ...
    
    @factor.setter
    def factor(self, value : float):
        '''Sets the factor.'''
        ...
    
    @property
    def bias(self) -> int:
        '''Gets the bias.'''
        ...
    
    @bias.setter
    def bias(self, value : int):
        '''Sets the bias.'''
        ...
    
    @property
    def size(self) -> int:
        '''Gets the size.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Sets the size.'''
        ...
    
    @property
    def sigma(self) -> float:
        '''Gets the sigma.'''
        ...
    
    @sigma.setter
    def sigma(self, value : float):
        '''Sets the sigma.'''
        ...
    
    ...

class SmallRectangularFilterOptions(FilterOptionsBase):
    '''Small rectangular filter options'''
    
    def __init__(self):
        ...
    
    ...

