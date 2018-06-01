from __future__ import print_function
from bioblend.galaxy import GalaxyInstance
import time
import optparse

usage = "Usage: submit_topmed_rnaseq_workflow.py -k <API_KEY> --input-minid <INPUT_MINID>"
parser = optparse.OptionParser(usage = usage)
parser.add_option("-k", "--key",
                    action="store", type="string",
                    dest="api_key", help="User API Key")
parser.add_option("-m", "--input-minid",
                    action="store", type="string",
                    dest="input_minid", help="Input MINID containing BDBag of paired-ended fastq files")
(opts, args) = parser.parse_args()

if not opts.api_key:   # if api_key is not given
    parser.error('API_KEY is not given')
if not opts.input_minid:   # if minid is not given
    parser.error('Input MINID is not given')

URL="https://nihcommons.globusgenomics.org"
API_KEY = opts.api_key
input_minid = opts.input_minid
gi = GalaxyInstance(URL, API_KEY)
published_workflow_id = "6f1411e6cfea8ef7"
workflow_name = "imported: RNA-seq-Gtex-stage1-v2.0-bags_transfer"

# check if workflow exists
workflows = gi.workflows.get_workflows(name=workflow_name)
wf_mine = None
if len(workflows) > 0:
    wf_mine = workflows[-1]
else:
    # workflow does not exist, need to import from published
    wf_mine = gi.workflows.import_shared_workflow(published_workflow_id)

# create a history
history_name = "topmed_history_%s" % time.strftime("%a_%b_%d_%Y_%-I:%M:%S_%p",time.localtime(time.time()))
history = gi.histories.create_history(name=history_name)
wf_data = {}
wf_data['workflow_id'] = wf_mine['id']
wf_data['ds_map'] = {}
parameters = {}
parameters['0'] = {'minid' : input_minid}
parameters['5'] = {'historyid' : history['id'], 'userapi' : API_KEY, 'url' : URL}
wf_data['parameters'] = parameters
res = gi.workflows.invoke_workflow(wf_data['workflow_id'], wf_data['ds_map'], params=wf_data['parameters'], history_id=history['id'], import_inputs_to_history=False)
print ("SUBMITTED\t%s\t%s\t%s\t%s\t%s" % (input_minid, wf_mine['name'], wf_mine['id'], history_name, res['history_id']))
# loop until status is complete
done = 0
minid = None
while not done:
    state = gi.histories.show_history(history['id'], contents=False)['state']
    if state == 'ok':
        done = 1
        for content in gi.histories.show_history(history['id'], contents=True):
            if "Minid for history" in content['name'] and content['visible'] is True and content['deleted'] is False:
                id = content['id']
                dataset_content = gi.datasets.show_dataset(id)['peek']
                minid = dataset_content.split("\t")[-1].split("<")[0]
                print ("Your workflow is complete\nYour output MINID is: %s" % minid)
                break
    elif state == 'error':
        done = 1
        print ("There was an error with your submission. Please check your data.")
    else:
        print ("Workflow running: %s" % (time.strftime("%a_%b_%d_%Y_%-I:%M:%S_%p",time.localtime(time.time()))))
        time.sleep(60)
    
