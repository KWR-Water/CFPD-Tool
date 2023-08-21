# CFPD Tool

'CFPD Tool' is a GUI tool written in Python that applies CFPD (Comparison of Flow Pattern Distribution) analyses on flow data for drinking water DMAs and supply areas.

The code was written in 2010-2014 as I was learning Python. Therefore, there is room for improvement in terms of coding standards. But the tool functions and is usable for research and operational purposes.  

The CFPD method is described in the following publication:
van Thienen, P. (2013). A method for quantitative discrimination in flow pattern evolution of water distribution supply areas with interpretation in terms of demand and leakage. Journal of Hydroinformatics, 15(1), 86-102.
https://iwaponline.com/jh/article/15/1/86/3218/A-method-for-quantitative-discrimination-in-flow


## Installation

Download the source code and install the required dependencies. 

## Dependencies

The CFPD Tool uses the following non-standard libraries:
- calendar
- numpy
- pygame
- wx
- xlrd
- openpyxl

## Usage

Running cfpdtool.py launches the application GUI. 

Basic and advanced functionalities are described in the report "KWR 2014.087 Roaming CFPD tool for Windows Reference Manual.pdf"

## License

`CFPD Tool` is available under a [EUPL-1.2 license](https://github.com/KWR-Water/CFPD-Tool/blob/master/LICENSE).

## Development and contributions

The code was written in 2010-2014 and was slighly sanitized and updated to run on Python3 in 2023. It is not actively developed or maintained by the original developer because of a shifted work focus and lack of time. However, further cleaning up of the code, development and application are encouraged! 

## Citing

If you publish work based on `CFPD Tool` , I would appreciate a citation of the following reference:

van Thienen, P. (2013). A method for quantitative discrimination in flow pattern evolution of water distribution supply areas with interpretation in terms of demand and leakage. Journal of Hydroinformatics, 15(1), 86-102.
https://iwaponline.com/jh/article/15/1/86/3218/A-method-for-quantitative-discrimination-in-flow