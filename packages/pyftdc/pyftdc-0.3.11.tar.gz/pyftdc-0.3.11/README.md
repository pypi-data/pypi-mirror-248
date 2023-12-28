pyftdc
==============


|            | Link | status |
|--------------|------|------|
| Conda builds | https://anaconda.org/jimper/pyftdc |      |
| Pypi builds  | https://pypi.org/project/pyftdc/ |      |



A MongoDB FTDC files parser written in C++ that provides Python bindings using [pybind11](https://github.com/pybind/pybind11) and scikit-build.



[gitter-badge]:            https://badges.gitter.im/pybind/Lobby.svg
[gitter-link]:             https://gitter.im/pybind/Lobby
[actions-badge]:           https://github.com/pybind/pyftdc/workflows/Tests/badge.svg
[actions-conda-link]:      https://github.com/pybind/pyftdc/actions?query=workflow%3AConda
[actions-conda-badge]:     https://github.com/pybind/pyftdc/workflows/Conda/badge.svg
[actions-pip-link]:        https://github.com/pybind/pyftdc/actions?query=workflow%3APip
[actions-pip-badge]:       https://github.com/pybind/pyftdc/workflows/Pip/badge.svg
[actions-wheels-link]:     https://github.com/pybind/pyftdc/actions?query=workflow%3AWheels
[actions-wheels-badge]:    https://github.com/pybind/pyftdc/workflows/Wheels/badge.svg



Requisites
------------

To build the source distribution, you will need Python 3.8 or newer, git, python3-dev/python3-devel installed.

Please read the [build document](docs/build.md) for more details.


Installation
------------
You can install the source distributions via pip or conda:

- pip3 install pyftdc

- conda install -c jimper pyftdc

Building
------------

**Building on Unix (Ubuntu, Centos, macOS)**

  
 1. clone this repository and change to the top level directory.
      ```
      git clone git@gitlab.com:jimper/mongo_ftdc.git 
      cd mongo_ftdc
      ```
      
 2. Install Python libraries to build binaries. Create a virtual environment to make your life easier.
 
      ```
      python3 -m venv venv
      source venv/bin/activate
      pip3 install --user-pep517 .
      ```
      
    You will now have built and installed in your virtual environment.
    

Alternatively, you can use setup.py directly, but for that you will need to manually install the required libraries into your virtual environment by running

     
     cd mongo_ftdc
     pip install -r requirements.txt
     
     
After which you can create a source distribution or a binary wheel:

     python3 setup.py sdist
     python3 setup.py bdist_wheel
     
These will reside in the _dist_ directory.


**Building on Windows**
  
  Not tested yet, but 'It should work'(TM)
  


License
-------

Apache V2

Usage
---------

The module provides two classes, FTDCParser and Dataset. 
The proper usage is to obtain a Dataset object from a file by calling FTDCParse.parse_file(), or a list of Dataset objects from the FTDCParse.parse_dir(), and then call the methods on these objects.


FTDCParser 
 - set_verbose(bool). 
  
   Set verbosity flag.


 - parse_dir(dir, only_metadata, only_metrics_names, lazy)
 
   Returns a list of Dataset objects.


 - parse_file(file_path, only_metadata, only_metrics_names, lazy)
   
   Returns a single Dataset object.


 - get_parsed_file_info():
   
   Returns information on the last parsed file (absolute path, samples, start timestamp, end timestamp).


 - dump_file_as_json(input_file, output_file)
   
   Dumps the contents of an FTDC file to a JSON file. (WIP)


 - dump_file_as_csv(input_file, output_file)
   Dumps file contents to an FTDC file as CSV file. (WIP)

 
 - get_metric(metric_name, start, end, rated_metric).

   Returns a list of the values of a metric for the last file parsed. If rated_metric is true, will convert values to metrics per second. start and end are ignored.

   
 - get_metrics_list(metric_name_list)
   
   Returns a list of lists of values for the metrics specified in the list metric_name_list for the last file parsed. If rated_metric is true, will convert values to metrics per second. start and end are ignored.


 - get_timestamps(start, end)

   Returns the timestamps of the last file parsed.

 
 - metadata.
   
   Contains a string with the metadata of the last file parsed.


 - get_metric_numpy(metric_name, start, end, rated_metric)

   Returns a list of the values of a metric for the last file parsed as a numpy array. If rated_metric is true, will convert values to metrics per second. start and end are ignored.


 - get_metrics_list_numpy(metric_names_list, start, end, rated_metric)

   Returns a list of numpy arrays of the values of a metric for the last file parsed . If rated_metric is true, will convert values to metrics per second. start and end are ignored.


Dataset
 - interinm
   
   Contains a boolean that tells if this is an interim FTDC file.


 - metadata

   Contains the metadata associated with this datased.


 - metrics_names

   Contains a list of the metrics names contained in the dataset.


 - file

  Contains the file name from which this dataset was parsed.


 - path

   Contains the full path to the file from which this dataset was parsed.


- get_metric(metric_name, start, end, rated_metric)

  Returns a list of the values of a metric for this dataset. If rated_metric is true, will convert values to metrics per second. start and end are ignored.


- get_metric_numpy(metric_name, start, end, rated_metric)

  Returns a list of the values of a metric for the last file parsed as a numpy array. If rated_metric is true, will convert values to metrics per second. start and end are ignored.


- get_metrics_list_numpy(metric_names_list, start, end, rated_metric)

  Returns a list of numpy arrays of the values of a metric for the last file parsed . If rated_metric is true, will convert values to metrics per second. start and end are ignored.


 

Example
---------

```python
import pyftdc
import numpy

def get_prefixed_metrics_names(param, ds):
    ops_counters = []
    for name in ds.metrics_names:
        if name.startswith(param):
            ops = ds.get_metric(name)
            ops_counters.append((name, ops))

    return ops_counters


def open_files_in_dir(dir_path, prefix):
    from os import listdir

    files_read = []
    try:
        dir_list = listdir(dir_path)
        for file_name in dir_list:
            if file_name.startswith(prefix):
                parser = pyftdc.FTDCParser()
                ds = parser.parse_file(dir_path + '/' + file_name)
                if ds:
                    print(f'File: {ds.file}')
                    print(f'{ds.metadata}')
                    ts = ds.get_metric("start")
                    if ts:
                        ts_size = len(ts)

                        print(f'Timestamp count {ts_size}. Start:{ts[0]}  Last: {ts[-1]}')

                        op_counter_names = get_prefixed_metrics_names('serverStatus.opcounters', ds)
                        cpu = get_prefixed_metrics_names('systemMetrics.cpu', ds)
                        disk = get_prefixed_metrics_names('systemMetrics.disks.nvme1n1', ds)

                        xxx = ds.get_metric_list_numpy(['systemMetrics.cpu.iowait_ms', 'xxx', 'systemMetrics.cpu.num_cpus'])
                        disk_n = ds.get_metric_numpy('systemMetrics.disks.nvme1n1.writes')

                        files_read.append(file_name)
                    else:
                        print(f'No timestamps on this dataset.')
    except FileNotFoundError as not_found:
        print('Path not found.')

    return files_read

 

if __name__ == "__main__":
    files = open_files_in_dir('/somepath/diagnostic.data/',
                              'metrics.2022-11-13T21')
    print(files)

```

[`cibuildwheel`]:          https://cibuildwheel.readthedocs.io
