from xml.dom.minidom import parseString
from xml.dom.minidom import Document
from xml.dom.minidom import getDOMImplementation,Element
import proot,pickle,uuid
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
        if self.id:
            e.setAttribute("id",str(self.id))
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
        self.geomRoot = SaveEntity(0,"GEOMROOT")
        self.matRoot = SaveEntity(0,"MATROOT")
        self.__geomTrack = {}
        self.__matTrack = {}
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
        assert isinstance(act.geometry,proot.pygfx.Geometry)
        self.__geomTrack[act.geometry._trackable_id] =act.geometry
        assert isinstance(act.material,proot.pygfx.Material)
        self.__matTrack[act._id] =act.material
        sav = SaveEntity(
            self.id,"Mesh",
            **self.__generics(act),
            geom=act.geometry._trackable_id,
            mat=act._id
            
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
        for k,v in self.__geomTrack.items():
            s = SaveEntity(
            f"GEO.{k}","GEOM",
            geom="TODO"
            )
            self.geomRoot.children.append(s)
        self.sceneRoot.toXML(self.dom,self.top_element)
        self.geomRoot.toXML(self.dom,self.top_element)
        with open("scene.xml","w") as f:
            self.top_element.writexml(f,addindent="    ",newl="\n")