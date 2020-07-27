import json
import os
import random
import simplejson as json

import web_app.plotly_visualization.graphs_navigator as util

from web_app import runner as r
from web_app.Visualize_Ball_Generation_Debug_Steps import Log, log_processing


def background_ball_generation(input_words):
    # TODO folder name collision
    outfolder_name = random.randint(0, 1000000)
    outfolder_path = f"out/{outfolder_name}"
    if not os.path.isdir(outfolder_path):
        os.mkdir(outfolder_path)

    debug_circles_list = []
    r.run(f"--no_visualize_nballs --outfolder_path {outfolder_path}", input_words, debug_circles_list)

    log = [dcl["log"] for dcl in debug_circles_list]
    debug_circles_list = [dcl["circles"] for dcl in debug_circles_list]
    print(debug_circles_list)

    input_words = input_words
    word_senses_cumulative = input_words  # hack me

    out = {
        "plotly_json": util.plot_balls_json(outfolder_path),
        "plotly_full_tree": util.plot_combined_tree_json(word_senses_cumulative, outfolder_path),
        "plotly_animation": util.plot_animation_json(debug_circles_list),
        "generation_log": log}
    out = json.dumps(out)

    return out


def generate_animation_from_log(json_input):
    # ball_generation_log, childrenDic
    sample_children = {'*root*': ['tank', 'flower', 'animal'], 'animal': ['human', 'chicken'], 'chicken': [],
                       'human': ['kant', 'socrates'], 'socrates': [], 'kant': [], 'tank': [], 'flower': []}
    sample_log = [{"key": "human", "op": 0, "op_args": [], "vec": [0.002103641430607005617858040, 0.0004052266247240675744703609, -0.001591181944132624640202640, 0.001066819031837562005509454, 0.003514571498026449591691802, 0.003263715301302595108332352, 0.002986161420952353976097889, -0.003518652672593539236449394, 0.005551077607004809463692269, 0.0009980852501701392855630973, 0.002749487305849141003175194, -0.0002003278546044628612160945, 0.00007227420060437398011778163, 0.001393925173389897659336423, 0.001851594891301083437067073, -0.001132900050036375554505687, 0.001826733736229888099564334, -0.001218332637640811547492864, 0.0009990035144477347678150632, 0.0003066016403315099672156525, -0.003130566981051254170783233, 0.002359803154268078096249395, 0.001329714693534334166779379, -0.002189958272700978521464438, 0.002647015814427099950623761, -0.005854785014372491080100934, -0.001645835673543583819254699, -0.001711610603649865540833610, -0.0007654923096340169980030199, 0.0003373498897157340493378827, 0.01091544147756521009957996, -0.001073144852416552758599099, -0.002440338332392005023993592, -0.005697319695658899929144861, -0.004603905009559128550566168, 0.0005167787295578855667160802, 0.0001855472007139819874327942, -0.0005553798390049536991947080, -0.00009520359971381303878105819, 0.001332163398274588786117955, -0.001870776411766410594815899, -0.0002693745263220291315780306, 0.002155846455277709830703182, 0.001749667556487988202348110, 0.002384902377855686903864770, 0.0009399625223771530759830642, -0.001817653122818110726284620, 0.0002204106344533559986077995, -0.0007473310828104624248777634, -0.001770141448899560853636739, 0.002147964685819752161658883, 0.002147964685819752161658883, 0.001952695168927047419689894, 0.001952695168927047419689894, 0.001952695168927047419689894, 0.001952695168927047419689894, 0.001952695168927047419689894, 0.001952695168927047419689894, 0.001952695168927047419689894, 0.001952695168927047419689894, 0.001952695168927047419689894, 0.001952695168927047419689894, 0.001952695168927047419689894, 0.001952695168927047419689894, 0.001952695168927047419689894, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, -0.09997799264906482788812255, 10, 0.05000000000000000277555756156289135105907917022705078125]}, {"key": "animal", "op": 0, "op_args": [], "vec": [0.001918835154447139567224380, -0.002517495336867598242482113, -0.004200398633224433459181077, -0.0003943791337938664221900126, 0.003158279307219004475415233, 0.003566995987180194238039093, -0.002172118921510833858820070, -0.005333489882889908430287141, 0.007000664388707390254863397, 0.0002644832842585461151219910, 0.002469690634417523630661447, 0.0009455824248572586272484157, 0.003983596385249558947385275, 0.0003942631967628639106561810, 0.001874238043188136695818181, -0.0003241212930062868958787910, 0.002383974522829596702548806, 0.001383978984755114756155628, -0.002906000327757332644183046, -0.001371148619990826233589596, -0.0005477251801333139973784875, 0.0001635137239583761528773361, 0.001632470687870701595567229, -0.0008120616108192569138808676, 0.001118212664020139823463882, -0.004333726218877430986658905, -0.002039718832105857464218337, -0.0001789217553786225140418450, 0.0002498172498367164391297019, -0.001697472716586162799746393, 0.009276508307288554000851745, -0.001148356292080817623356483, -0.0007638318059221724860829774, -0.003428837691902087033725309, -0.002432938595589697817181711, 0.002476878730339685589391663, 0.0005696759246698075516116114, -0.00003456121539864701104749099, 0.001529170793247379009579689, 0.0002353483083675911107903349, -0.001310745426838468295704802, -0.0006143503272828119239394579, 0.0008546491468742143442573408, 0.003239010126473819418585585, 0.006195674936779291747573471, -0.00003961954806129073304615385, -0.001423822677743010318818720, -0.001236854892412806909491969, 0.001800115634700470286537684, -0.0004178757054103947642976946, 0.002147965545794305056884390, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, 10, 0.05000000000000000277555756156289135105907917022705078125]}, {"key": "animal", "op": 2, "op_args": ["human"], "vec": [0.001918835154447139567224380, -0.002517495336867598242482113, -0.004200398633224433459181077, -0.0003943791337938664221900126, 0.003158279307219004475415233, 0.003566995987180194238039093, -0.002172118921510833858820070, -0.005333489882889908430287141, 0.007000664388707390254863397, 0.0002644832842585461151219910, 0.002469690634417523630661447, 0.0009455824248572586272484157, 0.003983596385249558947385275, 0.0003942631967628639106561810, 0.001874238043188136695818181, -0.0003241212930062868958787910, 0.002383974522829596702548806, 0.001383978984755114756155628, -0.002906000327757332644183046, -0.001371148619990826233589596, -0.0005477251801333139973784875, 0.0001635137239583761528773361, 0.001632470687870701595567229, -0.0008120616108192569138808676, 0.001118212664020139823463882, -0.004333726218877430986658905, -0.002039718832105857464218337, -0.0001789217553786225140418450, 0.0002498172498367164391297019, -0.001697472716586162799746393, 0.009276508307288554000851745, -0.001148356292080817623356483, -0.0007638318059221724860829774, -0.003428837691902087033725309, -0.002432938595589697817181711, 0.002476878730339685589391663, 0.0005696759246698075516116114, -0.00003456121539864701104749099, 0.001529170793247379009579689, 0.0002353483083675911107903349, -0.001310745426838468295704802, -0.0006143503272828119239394579, 0.0008546491468742143442573408, 0.003239010126473819418585585, 0.006195674936779291747573471, -0.00003961954806129073304615385, -0.001423822677743010318818720, -0.001236854892412806909491969, 0.001800115634700470286537684, -0.0004178757054103947642976946, 0.002147965545794305056884390, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, 0.001952695950722095506258536, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, -0.09997803267697128992043705, 10.00162352170251289719251, 0.2871108816966982715209862]}]

    input_str = json.loads(json_input)
    children = input_str["children"]
    log = input_str["log"]
    log = [Log(l["key"], l["op"], l["op_args"], l["vec"]) for l in log]

    debug_circles_list = []
    log_processing(log, children, debug_circles_list)

    log = [dcl["log"] for dcl in debug_circles_list]
    debug_circles_list = [dcl["circles"] for dcl in debug_circles_list]

    out = {
        "plotly_animation": util.plot_animation_json(debug_circles_list),
        "generation_log": log}
    out = json.dumps(out)
    return out


if __name__ == '__main__':
    generate_animation_from_log("lol")