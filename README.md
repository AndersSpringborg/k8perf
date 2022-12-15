# Benchmark application
This is a benchmark application for kubernetes. It is used to test network performance of a kubernetes cluster.

<img alt="k8perf logo" src="./assets/logo.png"/>

## Demo of the application
[![k8perf demo video](https://img.youtube.com/vi/RA5H2KPW4Ic/0.jpg)](https://www.youtube.com/watch?v=RA5H2KPW4Ic)


## Run the application
install this python package, a place where you have a kubernetes config file, and run the following command:
```
pip install k8perf
python -m k8perf run
```

You can get a json output from the command line by adding the `--json` flag.


## Contributing
If you want to contribute, here is how to get your envirorment setup
#### Virtualenv
you can activate the virtualenv with the following command:
```bash
source bin/activate
```
if you're not using the script, remember to install the module with the following command:
```bash
    pip install --editable .
```

### Run iperf 3 benchmark on kubernetes without tool
There are two files in the folder `benchmarks/bandwidth`:
- the server `iperf3-server.yaml`
- the client `iperf3-client.yaml`


## Results
- The results of our experiments are located in the `results` folder. 
- Images and visualizations of data and analysis are located in the `results/images` folder.

#### TODO
- [ ] add a way to specify the namespace
- [ ] Run http benchmark until the server is up to 90% cpu usage
- [ ] loading bar for the benchmark
- [ ] Stream the output of the benchmark (Use streamlit)