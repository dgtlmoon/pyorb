# pyorb

Experimental Python ORB search server based on OpenCV2

This project is mostly just for personal research and learning.

Inspiration taken from the http://pastec.io project.

### Problems and improvements
 - The image that is received via do_PUT is written to disk and then read again
 - The pickle store for each _descriptors_ result is 200kb~ , could this be replaced with a system?
 - The distance search is brute force and needs to load the pickled list of _descriptors_ (again, could be a LSH system here?)
 - Could one of the mechanisms from https://github.com/ekzhu/datasketch be better here?
    - Scan across all entries efficiently (grouped by descriptors) without bruteforcing individual sets of 200 descriptors 
        
### Features
  - SciKit ORB ( oriented FAST detection method and the rotated BRIEF descriptors. ) matching http://scikit-image.org/docs/dev/auto_examples/plot_orb.html
  - Records a tag against each image uploaded (as it is in the list) so you can reference by an arbitrary tag
  
## Usage

Start the server `python ./http-server.py`

Use curl to upload all images in `./load-all-images.sh`

Upload a single file and get results `curl -X POST  --data-binary @images/c.jpg http://localhost:8080`
