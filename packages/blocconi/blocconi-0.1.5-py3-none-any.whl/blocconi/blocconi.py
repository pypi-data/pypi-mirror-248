# BLOCCONI (BLOCk and CONnect Illustrator)

from collections import OrderedDict
import matplotlib
from matplotlib import path as path
from matplotlib import patches as patches
from matplotlib import pyplot as plt

matplotlib.rcParams['figure.max_open_warning'] = 100

zo=10
depth=0
treedict={}

class blocconi:
    def make_canvas(mydict, w=400, h=300, fc="#000000", ec="#000000", alpha=1, linewidth=3, text="", textcolor="#000000", textrotate=0, fontsize=16, textpos_h="middle", textpos_v="middle", ellipse=False):
        mydict["_type"] = "block"
        #mydict["_x"] = x
        #mydict["_y"] = y
        mydict["_w"] = w
        mydict["_h"] = h
        mydict["_fc"] = fc
        mydict["_ec"] = ec
        mydict["_alpha"] = alpha
        mydict["_linewidth"] = linewidth
        mydict["_text"] = text
        mydict["_textcolor"] = textcolor
        mydict["_textrotate"] = textrotate
        mydict["_fontsize"] = fontsize
        mydict["_textpos_h"] = textpos_h
        mydict["_textpos_v"] = textpos_v
        mydict["_ellipse"] = False

    def add_block(mydict, blockid, x=50, y=50, w=50, h=50, fc="#000000", ec="#000000", alpha=1, linewidth=3, text="", textcolor="#000000", textrotate=0, fontsize=16, textpos_h="middle", textpos_v="middle", ellipse=False):
        mydict[blockid] = OrderedDict()
        mydict[blockid]["_type"] = "block"
        mydict[blockid]["_x"] = x
        mydict[blockid]["_y"] = y
        mydict[blockid]["_w"] = w
        mydict[blockid]["_h"] = h
        mydict[blockid]["_fc"] = fc
        mydict[blockid]["_ec"] = ec
        mydict[blockid]["_alpha"] = alpha
        mydict[blockid]["_linewidth"] = linewidth
        mydict[blockid]["_text"] = text
        mydict[blockid]["_textcolor"] = textcolor
        mydict[blockid]["_textrotate"] = textrotate
        mydict[blockid]["_fontsize"] = fontsize
        mydict[blockid]["_textpos_h"] = textpos_h
        mydict[blockid]["_textpos_v"] = textpos_v
        mydict[blockid]["_eclipse"] = False

    def add_canvas(mydict, blockid, x=0, y=0, canvas={}):
        mydict[blockid] = canvas.copy() # 辞書型はミュータブルなので、オリジナルに変更が加わらないように .copy() を使う。
        mydict[blockid]["_x"] = x
        mydict[blockid]["_y"] = y

    def add_connector(mydict, connectorid, block_from, edgepoint_from, block_to, edgepoint_to, color="#000000", linewidth=1, curve=0):
        mydict[connectorid] = OrderedDict()
        mydict[connectorid]["_type"] = "connector"
        mydict[connectorid]["_block_from"] = block_from
        mydict[connectorid]["_edgepoint_from"] = edgepoint_from
        mydict[connectorid]["_block_to"] = block_to
        mydict[connectorid]["_edgepoint_to"] = edgepoint_to
        mydict[connectorid]["_color"] = color
        mydict[connectorid]["_linewidth"] = linewidth
        mydict[connectorid]["_curve"] = curve

    def recursive(rectid, ep, cd, tcd, mydict): # ep:edge point, cd: countdict, tcd: total countdict
        if ("." in rectid):
            idx = rectid.find(".")
            #print("rectid[idx+1:]=",rectid[idx+1:])
            #print("rectid[:idx]=",rectid[:idx])
            #exit()
            x, y = blocconi.recursive(rectid[idx+1:], ep, cd, tcd, mydict[rectid[:idx]])
            x = x + mydict[rectid[:idx]]["_x"]
            y = y + mydict[rectid[:idx]]["_y"]
        else:
            # print("rectid=",rectid)
            if (ep == "R"):
                x = mydict[rectid]["_x"] + mydict[rectid]["_w"]
                y = mydict[rectid]["_y"] + mydict[rectid]["_h"] * cd / tcd
            if (ep == "L"):
                x = mydict[rectid]["_x"]
                y = mydict[rectid]["_y"] + mydict[rectid]["_h"] * cd / tcd
            if (ep == "T"):
                x = mydict[rectid]["_x"] + mydict[rectid]["_w"] * cd / tcd
                y = mydict[rectid]["_y"]
            if (ep == "B"):
                x = mydict[rectid]["_x"] + mydict[rectid]["_w"] * cd / tcd
                y = mydict[rectid]["_y"] + mydict[rectid]["_h"]
            if (ep == "TR"):
                x = mydict[rectid]["_x"] + mydict[rectid]["_w"]
                y = mydict[rectid]["_y"]
            if (ep == "TL"):
                x = mydict[rectid]["_x"]
                y = mydict[rectid]["_y"]
            if (ep == "BR"):
                x = mydict[rectid]["_x"] + mydict[rectid]["_w"]
                y = mydict[rectid]["_y"] + mydict[rectid]["_h"]
            if (ep == "BL"):
                x = mydict[rectid]["_x"]
                y = mydict[rectid]["_y"] + mydict[rectid]["_h"]
        return x, y

    def addstring(ax1, mydict, rel_x, rel_y): # rel_x: relative_x, rel_y: relative_y
        global zo
        #if ("_x" in mydict.keys()) and ("_y" in mydict.keys()) and ("_w" in mydict.keys()) and ("_h" in mydict.keys()) and ("_text" in mydict.keys()):
        if (mydict["_type"] == "block"):
            x = mydict["_x"]+rel_x
            y = mydict["_y"]+rel_y
            zo += 1
            # 長方形を描く
            ax1.add_patch(patches.Rectangle(xy=(x, y), width=mydict["_w"], height=mydict["_h"], ec=mydict["_ec"], fc=mydict["_fc"], alpha=mydict["_alpha"], linewidth=mydict["_linewidth"], zorder=zo))  # alphaは0だと透明、1だと不透明。エッジとフェイスの両方に対して作用する。
            # 位置を定めて文字を描く
            if (mydict["_textpos_h"] == "middle"):
                x_text = x + mydict["_w"] / 2
                horizontalalignment = "center"
            if (mydict["_textpos_h"] == "left"):
                x_text = x
                horizontalalignment = "left"
            if (mydict["_textpos_h"] == "right"):
                x_text = x+ mydict["_w"]
                horizontalalignment = "right"

            if (mydict["_textpos_v"] == "middle"):
                y_text = y + mydict["_h"] / 2
                verticalalignment = "center"
            if (mydict["_textpos_v"] == "top"):
                y_text = y
                verticalalignment = "top"
            if (mydict["_textpos_v"] == "bottom"):
                y_text = y + mydict["_h"]
                verticalalignment = "bottom"
            ax1.text(x_text, y_text, mydict["_text"], color=mydict["_textcolor"], fontsize=mydict["_fontsize"], ha=horizontalalignment, va=verticalalignment, rotation=mydict["_textrotate"], zorder=zo+0.1)

        for key, value in mydict.items():
            if key[0] != "_":
                if (value["_type"] == "block"):
                    blocconi.addstring(ax1, mydict[key], x, y)

        totalcountdict = {}
        for key, value in mydict.items():
            if key[0] != "_":
                if (value["_type"] == "connector"):
                    if ((value["_block_from"], value["_edgepoint_from"]) in totalcountdict):
                        totalcountdict[(value["_block_from"], value["_edgepoint_from"])] += 1
                    else:
                        totalcountdict[(value["_block_from"], value["_edgepoint_from"])] = 1
                    if ((value["_block_to"], value["_edgepoint_to"]) in totalcountdict):
                        totalcountdict[(value["_block_to"], value["_edgepoint_to"])] += 1
                    else:
                        totalcountdict[(value["_block_to"], value["_edgepoint_to"])] = 1

        countdict = {}
        for key, value in mydict.items():
            if key[0] != "_":
                if (value["_type"] == "connector"):
                    if ((value["_block_from"], value["_edgepoint_from"]) in countdict):
                        countdict[(value["_block_from"], value["_edgepoint_from"])] += 1
                    else:
                        countdict[(value["_block_from"], value["_edgepoint_from"])] = 1
                    if ((value["_block_to"], value["_edgepoint_to"]) in countdict):
                        countdict[(value["_block_to"], value["_edgepoint_to"])] += 1
                    else:
                        countdict[(value["_block_to"], value["_edgepoint_to"])] = 1

                    x1, y1 = blocconi.recursive(rectid=value["_block_from"], ep=value["_edgepoint_from"], cd=countdict[(value["_block_from"], value["_edgepoint_from"])], tcd=totalcountdict[(value["_block_from"], value["_edgepoint_from"])] + 1, mydict=mydict)
                    x2, y2 = blocconi.recursive(rectid=value["_block_to"], ep=value["_edgepoint_to"], cd=countdict[(value["_block_to"], value["_edgepoint_to"])], tcd=totalcountdict[(value["_block_to"], value["_edgepoint_to"])] + 1, mydict=mydict)

                    zo += 1
                    if value["_curve"] == 0:
                        ax1.plot([x1+x, x2+x], [y1+y, y2+y], color=value["_color"], linewidth=value["_linewidth"], zorder=zo)
                    else:
                        adx1 = 0
                        ady1 = 0
                        adx2 = 0
                        ady2 = 0
                        if (value["_edgepoint_from"] == "R"):
                            adx1 = 1
                        if (value["_edgepoint_from"] == "L"):
                            adx1 = -1
                        if (value["_edgepoint_from"] == "T"):
                            ady1 = -1
                        if (value["_edgepoint_from"] == "B"):
                            ady1 = 1
                        if (value["_edgepoint_from"] == "TR"):
                            adx1 = 1
                            ady1 = -1
                        if (value["_edgepoint_from"] == "TL"):
                            adx1 = -1
                            ady1 = -1
                        if (value["_edgepoint_from"] == "BR"):
                            adx1 = 1
                            ady1 = 1
                        if (value["_edgepoint_from"] == "BL"):
                            adx1 = -1
                            ady1 = 1
                        if (value["_edgepoint_to"] == "R"):
                            adx2 = 1
                        if (value["_edgepoint_to"] == "L"):
                            adx2 = -1
                        if (value["_edgepoint_to"] == "T"):
                            ady2 = -1
                        if (value["_edgepoint_to"] == "B"):
                            ady2 = 1
                        if (value["_edgepoint_to"] == "TR"):
                            adx2 = 1
                            ady2 = -1
                        if (value["_edgepoint_to"] == "TL"):
                            adx2 = -1
                            ady2 = -1
                        if (value["_edgepoint_to"] == "BR"):
                            adx2 = 1
                            ady2 = 1
                        if (value["_edgepoint_to"] == "BL"):
                            adx2 = -1
                            ady2 = 1
                        Path = path.Path
                        ax1.add_patch(patches.PathPatch(Path([(x1+x, y1+y), (x1+x + adx1 * value["_curve"], y1+y + ady1 * value["_curve"]), (x2+x + adx2 * value["_curve"], y2+y + ady2 * value["_curve"]), (x2+x, y2+y)], [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]), fc="none", color=value["_color"], linewidth=value["_linewidth"], zorder=zo))

    def save_pdf(pdf, mydict, papersize="a4portrait"):

        if papersize == "a4portrait":
            fig1 = plt.figure(figsize=(8.27, 11.69), dpi=200)
            ax1 = fig1.add_subplot(111)
            ax1.xaxis.tick_top()
            ax1.axis('off')  # 軸を非表示にする
            fig1.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)  # この1行を入れる
            plt.xlim(0, 2500)
            plt.ylim(3500, 0)
        elif papersize == "a4landscape":
            fig1 = plt.figure(figsize=(11.69, 8.27), dpi=200)
            ax1 = fig1.add_subplot(111)
            ax1.xaxis.tick_top()
            ax1.axis('off')  # 軸を非表示にする
            fig1.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)  # この1行を入れる
            plt.xlim(0, 3500)
            plt.ylim(2500, 0)
        else:
            print("Error! Please select right papersize.")
            exit(-1)

        print("save_pdf start")

        mydict["_x"]=0
        mydict["_y"]=0
        blocconi.addstring(ax1, mydict, 0, 0)

        pdf.savefig()
