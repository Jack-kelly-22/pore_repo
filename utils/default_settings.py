def get_default_constants():
    constants = {
        "thresh": 200,
        "fiber_type": 'dark',
        "use_alt": False,
        "multi" : False,
        "alt_thresh":55,
        "min_ignore": 20.0,
        "warn_size": 5000.0,
        "scale": 2.59,
        "num_circles": 100,
        "crop": 0,
    }
    return constants

def get_default_options():
    #options put in by user these are just placeholders
    options ={
        "program_type": "light",
        "input_type":0,
        "job_name": "default_name",
        "frame_paths":[],
        #"name_ls_ls": [],
        "constants": get_default_constants(),
        "tags": ["NULL(lol)"],
        }
    return options


def update_constants(const,thresh,type,warn,ignore,alt,alt_thresh,multi,num):
    const['thresh'] = int(thresh)
    const['fiber_type'] = type
    const['warn_size'] = int(warn)
    const['min_ignore'] = int(ignore)
    const['use_alt'] = bool(alt)
    const['alt_thresh'] = int(alt_thresh)
    const['multi'] = bool(multi)
    const['num_circles'] = int(num)
    return const
