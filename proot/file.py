from xml.dom.minidom import parseString
from xml.dom.minidom import Document
from xml.dom.minidom import getDOMImplementation,Element
import proot
import pylinalg as la

impl = getDOMImplementation()


blacklist = [
    proot.pygfx.AxesHelper,
]

def parse(text:str) -> Document:
    return parseString(text)

def serialise(dom:Document) -> str:
    return dom.toxml()

class SaveEntity:
    def __init__(self,id,typ,**kwargs):
        self.typ = typ
        self.id =id
        self.values = kwargs
        self.children:list[SaveEntity] = []
    def toXML(self,doc:Document,parentXML:Element):
        e = doc.createElement(self.typ)
        for k,v in self.values.items():
            e.setAttribute(k,str(v))
        for c in self.children:
            c.toXML(doc,e)
        parentXML.appendChild(e)

class Saver:
    def __init__(self) -> None:
        self.id = 0
        self.dom = impl.createDocument(None, "some_tag", None)
        self.top_element = self.dom.documentElement
        self.sceneRoot = SaveEntity(0,"SCENEROOT")
    def __generics(self,act:proot.pygfx.WorldObject):
        eur = la.quat_to_euler(act.local.rotation)
        return {
            "x":act.local.x,
            "y":act.local.y,
            "z":act.local.z,
            "xr":eur[0],
            "yr":eur[1],
            "zr":eur[2],
            "xs":act.local.scale_x,
            "ys":act.local.scale_y,
            "zs":act.local.scale_z,
            "visible":act.visible
        }
    def _save_actor(self,parent:SaveEntity,act:proot.Actor):
        sav = SaveEntity(
            self.id,"Actor",
            **self.__generics(act),
        )
        parent.children.append(sav)
        return sav
    def _save_camera(self,parent:SaveEntity,act:proot.pygfx.PerspectiveCamera):
        sav = SaveEntity(
            self.id,"PerspectiveCamera",
            **self.__generics(act),
            fov = act.fov,
            aspect = act.aspect
        )
        parent.children.append(sav)
        return sav
    def _save_mesh(self,parent:SaveEntity,act:proot.pygfx.Mesh):
        sav = SaveEntity(
            self.id,"Mesh",
            **self.__generics(act),
        )
        parent.children.append(sav)
        return sav
    def _save_DirectionalLight(self,parent:SaveEntity,act:proot.pygfx.DirectionalLight):
        sav = SaveEntity(
            self.id,"DirectionalLight",
            **self.__generics(act),
            r = act.color.r,g = act.color.g,b = act.color.b,a = act.color.a,
            intensity=act.intensity
        )
        parent.children.append(sav)
        return sav
    def _save_AmbientLight(self,parent:SaveEntity,act:proot.pygfx.AmbientLight):
        sav = SaveEntity(
            self.id,"AmbientLight",
            **self.__generics(act),
            r = act.color.r,g = act.color.g,b = act.color.b,a = act.color.a,
            intensity=act.intensity
        )
        parent.children.append(sav)
        return sav
    def save(self,parent:SaveEntity,act: proot.pygfx.WorldObject):
        if type(act) in blacklist: return
        
        if isinstance(act,proot.Actor):
            ret =self._save_actor(parent,act)
        elif isinstance(act,proot.pygfx.PerspectiveCamera):
            ret =self._save_camera(parent,act)
        elif isinstance(act,proot.pygfx.Mesh):
            ret =self._save_mesh(parent,act)
        elif isinstance(act,proot.pygfx.AmbientLight):
            ret =self._save_AmbientLight(parent,act)
        elif isinstance(act,proot.pygfx.DirectionalLight):
            ret =self._save_DirectionalLight(parent,act)
        else:
            ret = SaveEntity(self.id,"Unknown",type=type(act))
            parent.children.append(ret)
        self.id +=1
        for I in act.children:
            self.save(ret,I)
    def toXML(self):
        assert self.top_element
        self.sceneRoot.toXML(self.dom,self.top_element)

        with open("scene.xml","w") as f:
            self.top_element.writexml(f,addindent="    ",newl="\n")