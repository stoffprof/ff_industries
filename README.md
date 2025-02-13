# Fama-French industry SIC code mapping

Python code to read the industry definitions files from Ken French's  [Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) and return a dictionary that maps from SIC code to Fama-French industry code.

## Installation and Use

To install, run this in a terminal:

```bash
pip install git+https://github.com/stoffprof/ff_industries.git
```

To use the mapping in Python, do:

```python
import ff_industries

ff_map = ff_industries.get_sic_map(num_ports)
```

where `num_ports` is the number of industry portfolios you want.