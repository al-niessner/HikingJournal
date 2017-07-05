# ${this['label']}

* Trail head: __${this['segs'][0]['th'].split ('ev')[0].strip()}__
* Trail end:  __${this['segs'][-1]['te'].split ('ev')[0].strip()}__
* Distance:   __${'%5.2f Km' % sum([float(s['walked'].split()[0]) for s in this['segs']])}__
* Elevation
    * Start:  __${this['segs'][0]['th'].split ('ev')[-1].strip()}__
    * Finish: __${this['segs'][-1]['te'].split ('ev')[-1].strip()}__
    * Gain:   __${str(sum([s['gain'] for s in this['segs']]))} m__
    * min:    __${str(min([s['elmm']['min'] for s in this['segs']]))} m__
    * max:    __${str(max([s['elmm']['max'] for s in this['segs']]))} m__
