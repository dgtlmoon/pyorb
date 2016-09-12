# pyorb

Experimental Python ORB image feature extraction and similar image search server based on SciKit's ORB functionality.

This project is mostly just for personal research and learning.

Inspiration taken from the http://pastec.io project.

### Problems and improvements
 - The image that is received via do_PUT is written to disk and then read again
 - The pickle store for each _descriptors_ result is 200kb~ , could this be replaced with a LSH system? Pickling with threads is probably bad too.
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

Results will come back as a JSON object where `id` is the ID sent from curl (via load-all-images.sh) and `d` is the number of _descriptiors_ out of 200 that match.


In this example, the 8 images takes about 1.4 seconds to check, probably 5ms extra per image

```
{"results":[...], "time":1480.000}
```

Example:

```
{"results": [{"id": "/images/g.jpg", "d": 78}, {"id": "/images/f.jpg", "d": 70}, {"id": "/images/h.jpg", "d": 68}, {"id": "/images/a.jpg", "d": 72}, {"id": "/images/c.jpg", "d": 200}, {"id": "/images/d.jpg", "d": 69}, {"id": "/images/g.jpg", "d": 78}, {"id": "/images/f.jpg", "d": 70}, {"id": "/images/h.jpg", "d": 68}, {"id": "/images/a.jpg", "d": 72}, {"id": "/images/c.jpg", "d": 200}, {"id": "/images/d.jpg", "d": 69}, {"id": "/images/g.jpg", "d": 78}, {"id": "/images/f.jpg", "d": 70}, {"id": "/images/h.jpg", "d": 68}, {"id": "/images/a.jpg", "d": 72}, {"id": "/images/c.jpg", "d": 200}, {"id": "/images/d.jpg", "d": 69}], "time": 1486.422607421875}
```

The goal eventually is to be able to scan 10,000+ images in under 500ms (or less!)


```
-- GOT POST--
>>> Actual time spent matching 135.257812 ms
127.0.0.1 - - [12/Sep/2016 15:50:16] "POST / HTTP/1.1" 200 -
```

## Credits

- Gil Levi @ http://gilscvblog.com for help understanding the features/descriptors in ORB and other systems
 