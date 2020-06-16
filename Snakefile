#configfile: "config.yaml"

gedfile = config['gedfile']
outdir = config['outdir']

rule all:
    input: outdir + "/cleaned.csv"

rule ged_cleanup:
    input: gedfile
    output: outdir + "/cleaned.ged"
    shell:
        "ged2csv/ged_cleanup.sh {input} {output}"

rule make_csv:
    input: outdir + "/cleaned.ged"
    output: outdir + "/cleaned.csv"
    shell:
        "ged2csv/ged2csv.py {input} {output}"
