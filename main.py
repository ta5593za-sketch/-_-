# -*- coding: utf-8 -*-
import os, json, random
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

TITLE = "آزمایشگاه علوم هفتم"
SECTIONS = [
("مواد مورد نیاز زندگی ما","ما در زندگی روزمره از وسایل مختلفی استفاده می‌کنیم. این وسایل از موادی مانند آهن، مس، آلومینیم، شیشه و پلاستیک ساخته شده‌اند. بسیاری از مواد اولیه از طبیعت به دست می‌آیند و انسان آن‌ها را به وسایل مورد نیاز تبدیل می‌کند."),
("معدن چیست؟","معدن محلی در پوسته زمین است که مواد معدنی ارزشمندی در آن وجود دارد. برای استفاده از بعضی مواد معدنی باید آن‌ها را استخراج کرد. مواد معدنی در ساخت ساختمان‌ها، خودروها و ابزارها کاربرد دارند."),
("سنگ معدن و استخراج فلزها","بعضی فلزها به صورت خالص در طبیعت یافت نمی‌شوند و در ترکیب با مواد دیگر وجود دارند. برای به دست آوردن آن‌ها سنگ معدن استخراج می‌شود. مراحل کلی: ۱. استخراج سنگ معدن ۲. خرد کردن سنگ‌ها ۳. جداسازی مواد باارزش ۴. انجام فرایندهای لازم ۵. تبدیل فلز به شکل مناسب."),
("کاربرد فلزها در زندگی","آهن: در ساختمان‌سازی، پل‌سازی، خودرو و ابزارها استفاده می‌شود.\\n\\nمس: رسانای خوب جریان الکتریکی است و در سیم برق کاربرد دارد.\\n\\nآلومینیم: فلزی نسبتاً سبک است و در وسایل حمل‌ونقل، ظروف و قطعات صنعتی کاربرد دارد."),
("از معدن تا خانه","مواد معدنی پس از استخراج و انجام مراحل مختلف، به شکل وسایل قابل استفاده درمی‌آیند. برای مثال سنگ معدن آهن پس از فرآوری به آهن تبدیل می‌شود و در کارخانه‌ها برای ساخت محصولات به کار می‌رود."),
("مصرف درست و بازیافت","بازیافت یعنی استفاده دوباره از مواد دورریختنی و تبدیل آن‌ها به مواد یا وسایل قابل استفاده. فواید بازیافت: کاهش مصرف منابع طبیعی، صرفه‌جویی در انرژی، کاهش زباله، کمک به حفظ محیط زیست و کاهش نیاز به استخراج مواد جدید.")
]
TIPS = ["بسیاری از مواد اولیه وسایل زندگی از طبیعت به دست می‌آیند.","معدن محلی برای استخراج مواد معدنی است.","برای به دست آوردن بعضی فلزها باید سنگ معدن را فرآوری کرد.","مس رسانای خوب جریان برق است.","آهن در ساختمان‌سازی و ساخت ابزارها کاربرد دارد.","آلومینیم فلزی سبک است.","بازیافت به حفظ منابع طبیعی کمک می‌کند."]
LABS = [
("تفکیک مواد برای بازیافت","وسایل: بسته‌بندی‌های تمیز کاغذی، پلاستیکی و فلزی.\\nروش: آن‌ها را بر اساس جنس جدا کن.\\nنتیجه: جداسازی بر اساس جنس، بازیافت را آسان‌تر می‌کند. از مواد تیز یا آلوده استفاده نکن."),
("ردیابی فلزها در خانه","وسایل: دفتر و مداد.\\nروش: پنج وسیله فلزی پیدا کن و نام وسیله و فلز احتمالی آن را بنویس.\\nنتیجه: فلزها در وسایل روزمره کاربردهای زیادی دارند. وسایل برقی را باز نکن."),
("مقایسه مواد","وسایل: قاشق فلزی و چوبی.\\nروش: ظاهر و کاربرد آن‌ها را مقایسه و تفاوت‌ها را یادداشت کن.\\nنتیجه: مواد مختلف ویژگی‌ها و کاربردهای متفاوتی دارند.")
]
Q = [
("معدن چیست؟",["محل وجود مواد معدنی در پوسته زمین","کارخانه لباس","نوعی فلز","ابزار"],0),
("کدام فلز رسانای خوب برق است؟",["مس","چوب","پلاستیک","کاغذ"],0),
("آلومینیم چه ویژگی‌ای دارد؟",["نسبتاً سبک است","چوبی است","مایع است","رسانای ضعیف نور است"],0),
("آهن در کجا کاربرد دارد؟",["ساختمان‌سازی","تهیه ابر","تولید باران","ساخت کاغذ"],0),
("بازیافت یعنی چه؟",["استفاده دوباره از مواد دورریختنی","دفن همه زباله‌ها","استخراج بیشتر","سوزاندن مواد"],0),
("کدام مورد از فواید بازیافت است؟",["کاهش مصرف منابع طبیعی","افزایش زباله","هدررفتن انرژی","آلودگی بیشتر"],0),
("برای به دست آوردن بعضی فلزها چه چیزی استخراج می‌شود؟",["سنگ معدن","چوب","پلاستیک","آب"],0),
("یکی از مراحل آماده‌سازی سنگ معدن چیست؟",["خرد کردن سنگ‌ها","دوختن","رنگ‌آمیزی لباس","یخ‌زدن"],0),
("مس در ساخت چه چیزی کاربرد دارد؟",["سیم برق","دفتر","لباس","ظرف سفالی"],0),
("آهن در ساخت کدام مورد کاربرد دارد؟",["پل","ابر","باران","نور"],0),
("مواد معدنی در ساخت چه چیزهایی کاربرد دارند؟",["خودرو و ساختمان","فقط غذا","فقط لباس","هیچ‌چیز"],0),
("کدام گزینه فلز است؟",["آلومینیم","چوب","کاغذ","پلاستیک"],0),
("چرا باید در مصرف مواد دقت کنیم؟",["برای حفظ منابع طبیعی","برای افزایش زباله","برای هدر دادن انرژی","دلیلی ندارد"],0),
("پس از استخراج سنگ معدن چه کاری ممکن است انجام شود؟",["جداسازی مواد باارزش","کاشت بذر","پخت نان","تبخیر آب"],0),
("کدام فلز در سیم‌های برق استفاده می‌شود؟",["مس","چوب","شیشه","کاغذ"],0),
("کدام فلز برای ساخت ظروف سبک کاربرد دارد؟",["آلومینیم","چوب","پارچه","کاغذ"],0),
("بازیافت چه اثری بر زباله دارد؟",["کاهش مقدار زباله","افزایش زباله","بی‌اثر است","تبدیل زباله به سنگ"],0),
("مواد اولیه بسیاری از وسایل از کجا می‌آیند؟",["طبیعت","ابرها","فضا","فقط آزمایشگاه"],0),
("سنگ معدن پس از فرآوری می‌تواند به چه چیزی تبدیل شود؟",["فلز","گیاه","ابر","آب"],0),
("کدام رفتار به بازیافت کمک می‌کند؟",["جداکردن مواد بر اساس جنس","مخلوط کردن همه زباله‌ها","ریختن زباله در طبیعت","شکستن وسایل"],0)
]
PALETTE = {"bg":(0.94,0.97,1,1),"blue":(0.12,0.38,0.76,1),"teal":(0.05,0.58,0.53,1),"dark":(0.08,0.16,0.29,1),"white":(1,1,1,1),"text":(0.12,0.17,0.24,1)}
class L(Label):
    def __init__(self, **kw):
        kw.setdefault("color", PALETTE["text"]); kw.setdefault("font_size", sp(16))
        kw.setdefault("halign","right"); kw.setdefault("valign","middle")
        kw.setdefault("size_hint_y",None); super().__init__(**kw)
        self.bind(texture_size=self.resize); self.resize()
    def resize(self,*a):
        self.text_size=(max(dp(120),self.width-dp(16)),None); self.height=max(dp(42),self.texture_size[1]+dp(18))
class B(Button):
    def __init__(self, **kw):
        kw.setdefault("size_hint_y",None); kw.setdefault("height",dp(54)); kw.setdefault("font_size",sp(16))
        kw.setdefault("color",PALETTE["white"]); kw.setdefault("background_normal","")
        kw.setdefault("background_color",PALETTE["blue"]); super().__init__(**kw)
class Page(Screen):
    def setup(self,title):
        self.clear_widgets(); box=BoxLayout(orientation="vertical",padding=dp(12),spacing=dp(9))
        head=BoxLayout(size_hint_y=None,height=dp(48))
        head.add_widget(L(text=title,bold=True,font_size=sp(20),color=PALETTE["dark"]))
        back=B(text="بازگشت",size_hint_x=None,width=dp(90)); back.bind(on_release=lambda *_:setattr(self.manager,"current","home")); head.add_widget(back)
        box.add_widget(head); sc=ScrollView(do_scroll_x=False); self.content=BoxLayout(orientation="vertical",spacing=dp(10),padding=dp(4),size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter("height")); sc.add_widget(self.content); box.add_widget(sc); self.add_widget(box)
    def card(self,title,body):
        self.content.add_widget(L(text=title,bold=True,color=PALETTE["blue"],font_size=sp(18)))
        self.content.add_widget(L(text=body,font_size=sp(15)))
class Home(Page):
    def on_pre_enter(self,*a):
        self.setup(TITLE); self.content.add_widget(L(text="درس پنجم: از معدن تا خانه\\nبا هم دنیای مواد را کشف کنیم!",bold=True,font_size=sp(21),color=PALETTE["dark"]))
        for title,screen in [("📘 شروع آموزش","lesson"),("🧪 آزمایشگاه","lab"),("📝 آزمون ۲۰ سؤالی","quiz"),("🎮 بازی علمی","game"),("⭐ نکته‌های مهم","tips"),("📊 پیشرفت من","progress")]:
            b=B(text=title,background_color=PALETTE["teal"] if screen in ("lab","game") else PALETTE["blue"]); b.bind(on_release=lambda _,s=screen:setattr(self.manager,"current",s)); self.content.add_widget(b)
class ContentPage(Page):
    dataset=[]
    def on_pre_enter(self,*a):
        self.setup(self.title)
        for t,b in self.dataset:self.card(t,b)
class Lesson(ContentPage):
    title="آموزش درس"
    def on_pre_enter(self,*a):
        super().on_pre_enter(); self.card("فعالیت پیشنهادی","پنج وسیله فلزی پیدا کن و نام وسیله و فلز احتمالی آن را بنویس. بررسی کن کدام‌یک قابلیت بازیافت دارند.")
        self.manager.data["read"]=True; self.manager.save()
class Lab(ContentPage):
    title="آزمایشگاه"; dataset=LABS
class Tips(ContentPage):
    title="نکته‌های مهم"; dataset=[(f"نکته {i+1}",x) for i,x in enumerate(TIPS)]
class Progress(ContentPage):
    title="پیشرفت من"
    def on_pre_enter(self,*a):
        super().on_pre_enter()
        d=self.manager.data
        self.card("گزارش یادگیری",f"وضعیت مطالعه: {'مطالعه شده' if d.get('read') else 'مطالعه نشده'}\\nبهترین نمره آزمون: {d.get('best',0)}٪\\nبهترین امتیاز بازی: {d.get('game',0)} از ۴")
class Quiz(Page):
    def on_pre_enter(self,*a):
        self.setup("آزمون علوم"); self.questions=Q[:]; random.shuffle(self.questions); self.i=0; self.score=0; self.nextq()
    def nextq(self):
        self.content.clear_widgets()
        if self.i>=len(self.questions):
            pct=round(self.score*100/len(self.questions)); self.manager.data["best"]=max(pct,self.manager.data.get("best",0)); self.manager.save()
            self.card("آزمون تمام شد",f"پاسخ درست: {self.score} از ۲۰\\nپاسخ نادرست: {20-self.score}\\nدرصد موفقیت: {pct}٪"); return
        q,opts,ans=self.questions[self.i]; self.card(f"سؤال {self.i+1} از ۲۰",q)
        for j,opt in enumerate(opts):
            b=B(text=opt); b.bind(on_release=lambda _,choice=j,a=ans:self.answer(choice,a)); self.content.add_widget(b)
    def answer(self,choice,ans):
        if choice==ans:self.score+=1; msg="آفرین! پاسخ درست بود."
        else:msg="پاسخ درست نبود. پاسخ صحیح: "+self.questions[self.i][1][ans]
        self.card("نتیجه",msg); b=B(text="سؤال بعدی",background_color=PALETTE["teal"]); b.bind(on_release=lambda *_:self.advance()); self.content.add_widget(b)
    def advance(self):self.i+=1; self.nextq()
class Game(Page):
    def on_pre_enter(self,*a):
        self.setup("بازی تطبیق مواد"); self.pairs=[("آهن","ساخت پل و ساختمان"),("مس","ساخت سیم برق"),("آلومینیم","ساخت ظروف سبک"),("بازیافت","کاهش مصرف منابع طبیعی")]; random.shuffle(self.pairs); self.i=0; self.score=0; self.ask()
    def ask(self):
        self.content.clear_widgets()
        if self.i==4:
            self.card("بازی تمام شد",f"امتیاز تو: {self.score} از ۴"); self.manager.data["game"]=max(self.score,self.manager.data.get("game",0)); self.manager.save(); return
        material,use=self.pairs[self.i]; self.card(f"مورد {self.i+1} از ۴",f"کاربرد مناسب «{material}» را انتخاب کن.")
        choices=[x[1] for x in self.pairs]; random.shuffle(choices)
        for c in choices:
            b=B(text=c); b.bind(on_release=lambda _,v=c,u=use:self.choose(v,u)); self.content.add_widget(b)
    def choose(self,v,u):
        if v==u:self.score+=1; result="درست بود!"
        else:result="پاسخ مناسب: "+u
        self.card("نتیجه",result); b=B(text="ادامه"); b.bind(on_release=lambda *_:self.advance()); self.content.add_widget(b)
    def advance(self):self.i+=1; self.ask()
class Manager(ScreenManager):
    def __init__(self,app,**kw):
        super().__init__(**kw); self.appref=app
        try:
            with open(app.path,"r",encoding="utf8") as f:self.data=json.load(f)
        except:self.data={"read":False,"best":0,"game":0}
        for n,c in [("home",Home),("lesson",Lesson),("lab",Lab),("quiz",Quiz),("game",Game),("tips",Tips),("progress",Progress)]:self.add_widget(c(name=n))
    def save(self):
        os.makedirs(os.path.dirname(self.appref.path),exist_ok=True)
        with open(self.appref.path,"w",encoding="utf8") as f:json.dump(self.data,f,ensure_ascii=False)
class ScienceApp(App):
    title=TITLE
    def build(self):
        Window.clearcolor=PALETTE["bg"]; self.path=os.path.join(self.user_data_dir,"progress.json"); return Manager(self)
if __name__=="__main__":ScienceApp().run()
