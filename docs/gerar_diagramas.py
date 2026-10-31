"""Gera as pranchas conceituais do projeto; requer matplotlib e numpy.

Geometria interna adotada: 200 × 125 × 230 mm; alturas calculadas com tubo externo de 54 mm.
Os nomes de redes no esquema elétrico identificam conexões comuns.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

OUT = Path(__file__).resolve().parent
plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none'})


def cad():
    bg, ink, muted = '#101b29', '#d6e5f3', '#859cb3'
    fig = plt.figure(figsize=(16, 10), facecolor=bg)
    ax = fig.add_axes([.01, .17, .69, .68], projection='3d', facecolor=bg)
    def line(points, color=ink, lw=1.2, **kw):
        a = np.array(points)
        ax.plot(a[:, 0], a[:, 1], a[:, 2], color=color, lw=lw, **kw)
    def face(v, color, alpha):
        ax.add_collection3d(Poly3DCollection([v], facecolors=color, edgecolors='none', alpha=alpha))
    def box(x,y,z,w,d,h,color=ink,alpha=0.05):
        pts = [(x,y,z),(x+w,y,z),(x+w,y+d,z),(x,y+d,z)]
        top = [(a,b,z+h) for a,b,_ in pts]
        for k in range(4):
            line([pts[k],pts[(k+1)%4]],color)
            line([top[k],top[(k+1)%4]],color)
            line([pts[k],top[k]],color)
        face([pts[0],pts[1],top[1],top[0]],color,alpha)
        face([pts[1],pts[2],top[2],top[1]],color,alpha)
        face(top,color,alpha)
    def tube(x,y,z0,z1,r=2.5,color='#ced8df'):
        t=np.linspace(0,2*np.pi,60)
        for z in [z0,z1]:
            line(list(zip(x+r*np.cos(t),y+r*np.sin(t),np.full_like(t,z))),color,1.8)
        for a in [0,np.pi/2,np.pi,3*np.pi/2]:
            line([(x+r*np.cos(a),y+r*np.sin(a),z0),(x+r*np.cos(a),y+r*np.sin(a),z1)],color)
        ri=r-.2
        line(list(zip(x+ri*np.cos(t),y+ri*np.sin(t),np.full_like(t,z1))),muted,.7)
    def call(n,p,off):
        q=tuple(p[i]+off[i] for i in range(3))
        line([p,q],muted,.8)
        ax.text(*q,str(n).zfill(2),color='#ffffff',fontsize=11,ha='center',va='center',
                bbox=dict(boxstyle='circle,pad=.35',fc=bg,ec='#a7bfd5',lw=.8))
    # Geometria interna escolhida para o projeto. Unidades da cena: cm.
    L,W,H=20.0,12.5,23.0
    area=.2*.125
    area_tubo=np.pi*.054**2/4
    heights=[v/1000/(area-area_tubo)*100 for v in [1,2,2.5]]
    crest=.0028/(area-area_tubo)*100
    for x in np.arange(-12,55,4): line([(x,-14,-5),(x,36,-5)],'#213247',.45)
    for y in np.arange(-14,37,4): line([(-12,y,-5),(54,y,-5)],'#213247',.45)
    box(0,0,0,L,W,H)
    face([(0,0,0),(L,0,0),(L,W,0),(0,W,0)],'#8aa2b8',.06)
    # Parede frontal transparente, sem tampa.
    face([(0,0,0),(L,0,0),(L,0,H),(0,0,H)],'#8ebde0',.055)
    levels=list(zip(heights,['#68bde4','#61dabd','#ffb76c']))
    for z,c in levels:
        line([(0,0,z),(L,0,z),(L,W,z)],c,.8,ls='--')
    face([(0,0,heights[1]),(L,0,heights[1]),(L,W,heights[1]),(0,W,heights[1])],'#4294bf',.12)
    # S1/S2/S3 externos na parede lateral esquerda.
    for i,(z,c) in enumerate(levels):
        box(-1.1,2+i*3.2,z-.48,1.1,2.5,.96,c,.17)
    # Tubo vertical, flange e queda livre, com crista ilustrativa.
    tube(14.5,8.2,-4,crest,r=2.7)
    tube(14.5,8.2,-.3,.4,3.2,'#f4cb76')
    line([(14.5,8.2,-4),(14.5,20,-4)],'#ced8df',3)
    # Entrada lateral próxima à base e válvula externa normalmente fechada.
    line([(-10,10,1.4),(0,10,1.4)],'#5ed0e7',3)
    box(-7.5,8.4,.2,3.8,3.2,2.4,'#e8bd72',.25)
    box(-6.8,8.8,2.6,2.4,2.4,2.2,'#d6e5f3',.15)
    # Dreno separado na parede frontal e registro manual.
    line([(8,0,1.2),(8,-8,1.2)],'#b0c4d3',3)
    box(7,-4.4,.6,2,2.5,1.2,'#e8bd72',.2)
    line([(6,-3.3,2.7),(10,-3.3,2.7)],'#e8bd72',2)
    line([(8,-3.3,1.8),(8,-3.3,2.7)],'#e8bd72',1.6)
    # Apoios separados preservam o vão sob a passagem de fundo.
    box(1,1,-4,3.5,3.5,4,'#66839b',.08)
    box(15.5,1,-4,3.5,3.5,4,'#66839b',.08)
    box(1,8,-4,3.5,3.5,4,'#66839b',.08)
    call(1,(13,12.5,23),(0,5,3))
    call(2,(-1,3,heights[0]),(-6,-4,-1))
    call(3,(-1,6.2,heights[1]),(-7,-1,1))
    call(4,(-1,9.4,heights[2]),(-7,3,3))
    call(5,(-6,10,3.8),(-8,8,-2))
    call(6,(8,-3.3,1.5),(0,-5,2))
    call(7,(14.5,8.2,crest),(8,5,3))
    call(8,(14.5,20,-4),(10,1,1))
    # Cotas internas principais — valores independentes da projeção.
    line([(0,-3,23),(20,-3,23)],'#6f8ea9',.8)
    for x in [0,20]: line([(x,-3.5,22.5),(x,-2.5,23.5)],'#6f8ea9',.8)
    ax.text(10,-3,24,'200 mm',color=ink,fontsize=9,ha='center')
    line([(23,0,0),(23,12.5,0)],'#6f8ea9',.8)
    ax.text(25,6,0,'125 mm',color=ink,fontsize=9)
    line([(23,0,0),(23,0,23)],'#6f8ea9',.8)
    ax.text(24,0,19,'230 mm',color=ink,fontsize=9)
    ax.set_xlim(-11,29);ax.set_ylim(-10,24);ax.set_zlim(-5,28)
    ax.set_box_aspect((40,34,33));ax.view_init(elev=24,azim=-58)
    ax.set_axis_off()
    fig.text(.05,.935,'CONTROLE DE NÍVEL DE ÁGUA',color='white',size=23,weight='bold')
    fig.text(.05,.895,'VISTA ISOMÉTRICA  /  CONJUNTO HIDRÁULICO',color='#89aac6',size=12)
    fig.text(.72,.81,'IDENTIFICAÇÃO DO CONJUNTO',color='white',size=11,weight='bold')
    items=[('01','Reservatório transparente','Dimensões internas: 200 × 125 × 230 mm'),
           ('02','S1 · início da reposição','1,0 L · altura calculada: 44,0 mm'),
           ('03','S2 · corte normal','2,0 L · altura calculada: 88,1 mm'),
           ('04','S3 · emergência','2,5 L · altura calculada: 110,1 mm'),
           ('05','Válvula solenoide de entrada','12 V CC · normalmente fechada'),
           ('06','Dreno com registro manual','Independente do extravasor'),
           ('07','Extravasor vertical aberto','2,8 L · crista: 123,3 mm · Ø int.: 50 mm'),
           ('08','Descarga por gravidade','Saída livre, visível e abaixo do tanque')]
    for i,(n,a,b) in enumerate(items):
        y=.755-i*.071
        fig.text(.72,y,n,color='#f4cb76',size=11,weight='bold')
        fig.text(.75,y,a,color=ink,size=10.6,weight='bold')
        fig.text(.75,y-.023,b,color=muted,size=8.4)
    fig.text(.05,.12,'GEOMETRIA DE EXEMPLO — DIMENSÕES INTERNAS ADOTADAS',color='#f4cb76',size=11,weight='bold')
    fig.text(.05,.083,'Alturas a partir do fundo interno; modelo com tubo de Ø externo 54 mm e Ø interno 50 mm.',color=ink,size=9)
    fig.text(.05,.058,'Exemplo calculado, sem vínculo com um recipiente comercial. ~5,47 L até a borda, sem descontar flanges.',color=muted,size=9)
    fig.text(.72,.08,'PRANCHA 01  /  REVISÃO A',color=ink,size=10,weight='bold')
    fig.text(.72,.054,'Enzo Castro Cordovil · 31/10/2026',color=muted,size=9)
    fig.savefig(OUT/'Vista_3D_Conceitual.png',dpi=170,facecolor=bg)
    fig.savefig(OUT/'Vista_3D_Conceitual.svg',facecolor=bg)
    plt.close(fig)


def eletrica():
    fig,ax=plt.subplots(figsize=(17,12),facecolor='#f5f7fa')
    fig.subplots_adjust(left=.025,right=.975,bottom=.025,top=.975)
    ax.set_xlim(0,160);ax.set_ylim(0,112);ax.axis('off')
    ink,muted='#1c3045','#61758a'
    red,black,green,blue,purple='#bf413c','#283745','#16825c','#2671b5','#8853a5'
    def txt(x,y,s,size=9,color=ink,ha='left',weight='normal',**kw):
        return ax.text(x,y,s,fontsize=size,color=color,ha=ha,va='center',weight=weight,**kw)
    def wire(points,c=black,lw=1.5,**kw):
        a=np.array(points);ax.plot(a[:,0],a[:,1],color=c,lw=lw,solid_capstyle='round',**kw)
    def dot(x,y,c=black): ax.add_patch(Circle((x,y),.33,color=c,zorder=6))
    def rect(x,y,w,h,title,sub='',fill='white'):
        ax.add_patch(Rectangle((x,y),w,h,facecolor=fill,edgecolor='#9baabd',lw=1.2))
        txt(x+w/2,y+h*.62,title,10,ha='center',weight='bold')
        if sub: txt(x+w/2,y+h*.27,sub,8,muted,ha='center')
    def net(x,y,s,c=black,side='left'):
        # Rótulos idênticos = mesma rede, sem cruzamentos implícitos.
        if side=='left':
            wire([(x,y),(x-3,y)],c);txt(x-3.4,y,s,7.6,c,ha='right',weight='bold',bbox=dict(fc='#f5f7fa',ec='none',pad=.4))
        else:
            wire([(x,y),(x+3,y)],c);txt(x+3.4,y,s,7.6,c,weight='bold',bbox=dict(fc='#f5f7fa',ec='none',pad=.4))
    def gnd(x,y):
        wire([(x,y),(x,y-1)],black)
        for w,dy in [(2,1),(1.3,1.6),(.6,2.2)]:wire([(x-w,y-dy),(x+w,y-dy)],black,1)
    txt(4,107,'DIAGRAMA DE CONEXÕES ELÉTRICAS',20,weight='bold')
    txt(4,102.5,'Arduino Uno R3  ·  3 × SEN0485  ·  relé DFR0017  ·  válvula 12 V CC',10,muted)
    wire([(4,99),(156,99)],'#c8d2dc',1)
    txt(4,96,'01  ALIMENTAÇÃO E CIRCUITO DA VÁLVULA',11,weight='bold')
    # Alimentação: fonte externa isolada, proteção e buck.
    rect(6,78,25,13,'FONTE ISOLADA','12 V CC · corrente a confirmar')
    txt(29.7,87,'+',9,ha='right');txt(29.7,81,'−',9,ha='right')
    wire([(31,87),(36,87)],red)
    ax.add_patch(Rectangle((36,86),6,2,fc='white',ec=red,lw=1.3))
    wire([(42,87),(47,87)],red);net(47,87,'+12V_PROT',red,'right')
    txt(39,90,'F1',8,red,ha='center');txt(39,82.8,'Dimensionar para a carga',7,muted,ha='center')
    wire([(31,81),(33,81)],black);gnd(33,81)
    rect(75,81,27,11,'CONVERSOR DC–DC','12 V → 5 V regulados')
    net(75,88,'+12V_PROT',red);net(75,84,'GND',black)
    net(102,88,'+5V',red,'right');net(102,84,'GND',black,'right')
    txt(132,88,'+5V → USB do Uno',9,blue,weight='bold')
    txt(132,84,'+5V → sensores / relé',8,muted)
    txt(132,80,'GND comum em todo o controle',8,muted)
    # Contato do mesmo módulo K1, mostrado separado para clareza.
    net(12,69,'+12V_PROT',red)
    wire([(12,69),(23,69)],red);dot(23,69,red)
    ax.add_patch(Circle((23,69),.55,fc='white',ec=red,lw=1.4))
    ax.add_patch(Circle((39,69),.55,fc='white',ec=red,lw=1.4))
    wire([(23.6,69),(36.5,72.5)],red)
    txt(23,65.8,'COM',8,ha='center');txt(39,65.8,'NO',8,ha='center')
    txt(31,76,'K1 · contatos do relé',8,ha='center',weight='bold')
    txt(31,63,'NC: sem ligação',7.6,muted,ha='center')
    # Nó positivo após NO -> V1; retorno -> GND; diodo antiparalelo.
    wire([(39.5,69),(69,69)],red)
    ax.add_patch(Rectangle((69,66),13,6,fc='#fff2de',ec=ink,lw=1.2,zorder=10))
    txt(75.5,69,'V1',9,ha='center',weight='bold',zorder=11)
    wire([(82,69),(103,69)],black);gnd(103,69)
    txt(110,73,'Válvula 12 V CC · normalmente fechada',9,weight='bold',zorder=11)
    txt(110,68,'D1 em paralelo com a bobina',8,muted,zorder=11)
    wire([(62,69),(62,77),(73,77)],red)
    wire([(78,77),(94,77),(94,69)],black)
    # Diodo aponta para a esquerda: cátodo no + após NO.
    ax.add_patch(Polygon([(78,75.5),(78,78.5),(74,77)],fc='white',ec=purple,lw=1.3,zorder=11))
    wire([(73.8,75.5),(73.8,78.5)],purple)
    wire([(73,77),(73.8,77)],red);wire([(78,77),(79,77)],black)
    txt(85,80,'D1 · 1N4001',8,purple,ha='center',zorder=11)
    txt(62,80,'K · faixa',7.5,purple,ha='center',zorder=11)
    txt(96,80,'A',7.5,purple,ha='center',zorder=11)
    dot(62,69,red);dot(94,69,black)
    wire([(4,60),(156,60)],'#c8d2dc',1)
    txt(4,57,'02  SENSORES, COMANDO E REARME',11,weight='bold')
    # Arduino central — esquema funcional, não disposição dos headers.
    rect(62,14,34,39,'ARDUINO UNO R3','',fill='#e9f3fb')
    # Remove título central para que não se sobreponha aos pinos.
    ax.add_patch(Rectangle((63,15),32,37,fc='#e9f3fb',ec='none',zorder=3))
    txt(79,48.6,'ARDUINO',12,blue,ha='center',weight='bold',zorder=4)
    txt(79,45.5,'UNO R3',10,blue,ha='center',zorder=4)
    txt(79,24,'D13 · LED integrado',8,muted,ha='center',zorder=4)
    txt(79,21,'Bloqueio de falha',8,muted,ha='center',zorder=4)
    txt(79,17,'USB: alimentação 5 V',8,blue,ha='center',weight='bold',zorder=4)
    net(62,51.5,'+5V',red)
    txt(63,51.5,'USB',7,red,zorder=4)
    # Sensores e sinais sem cruzamentos.
    for n,y,pin,vol in [(1,46,2,'1,0 L'),(2,35,3,'2,0 L'),(3,24,5,'2,5 L')]:
        rect(16,y-4,23,8,f'S{n} · SEN0485',vol)
        net(16,y+2,'+5V',red);net(16,y-2,'GND',black)
        target={2:40,3:34,5:28}[pin]
        wire([(39,y),(45+n*2,y),(45+n*2,target),(62,target)],green)
        txt(40,y+1.8,'OUT',7,green)
        txt(63,target,f'D{pin}',9,green,zorder=4)
        dot(62,target,green)
    # Rearme normalmente aberto.
    wire([(62,18.5),(45,18.5)],blue)
    txt(63,18.5,'D4',9,blue,zorder=4)
    wire([(45,18.5),(42,18.5)],blue)
    ax.add_patch(Circle((41.5,18.5),.5,fc='white',ec=blue,lw=1.2))
    ax.add_patch(Circle((34.5,18.5),.5,fc='white',ec=blue,lw=1.2))
    wire([(35,20.2),(41,20.2)],blue)
    wire([(34,18.5),(28,18.5)],black);gnd(28,18.5)
    txt(16,13.4,'B1 · rearme momentâneo NA',8,blue)
    txt(16,10.4,'D4 usa INPUT_PULLUP',7.8,muted)
    # Comando do módulo K1 e resistor de pull-down.
    txt(94.6,40,'D7',9,blue,ha='right',zorder=4)
    wire([(96,40),(116,40)],blue);dot(106,40,blue)
    rect(116,30,30,20,'K1 · DFR0017','Relé ativo em HIGH',fill='#f1ebfa')
    # Pin labels around module.
    txt(117,40,'D',9,blue)
    net(116,47,'+5V',red);txt(117,47,'+',8,red)
    net(116,33,'GND',black);txt(117,33,'−',8,black)
    txt(131,27,'COM / NO no circuito 01',8,muted,ha='center')
    wire([(106,40),(106,35)],blue)
    ax.add_patch(Rectangle((104.8,29),2.4,6,fc='white',ec=blue,lw=1.2))
    wire([(106,29),(106,25)],black);gnd(106,25)
    txt(102,32,'R1\n10 kΩ',8,blue,ha='right')
    # Terra da placa explicitado por rede nomeada.
    net(96,15.5,'GND',black,'right')
    txt(4,6.4,'Redes com o mesmo nome estão conectadas. GND = negativo da fonte, buck, Uno, sensores e relé.',8.6,weight='bold')
    txt(4,3.1,'Alimente o Uno pela USB do conversor; desconecte esse cabo antes de conectar a USB do computador. Não aplicar 12 V em 5V ou sinais.',8,muted)
    fig.savefig(OUT/'Diagrama_Eletrico.png',dpi=180,facecolor=fig.get_facecolor())
    fig.savefig(OUT/'Diagrama_Eletrico.svg',facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__=='__main__':
    cad()
    eletrica()
    print('Pranchas PNG e SVG geradas em', OUT)
