# supervisely_to_VOC_converter

 -h, --help show this help message and exit
  
 -i INPUT, --input INPUT Location of Jsons to read
 
 -s SUPERVISELY, --supervisely Location of Supervisely folder
 
 -o OUTPUT, --output OUTPUT Location of XMLs to write
 
 -p, --pretend         Pretend to be VOC2012
  
 -r, --overwrite       Overwrite the output dir if it exists



Example run commands: 

`python3 theConverter.py -i "inputFiles/" -o "ouputFiles/"` 

`python3 theConverter.py -s "Images Tagged as Valid" -p -r`
