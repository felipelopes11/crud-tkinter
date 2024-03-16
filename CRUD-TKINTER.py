import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as msb
from tkinter import Tk, Label, StringVar, Entry, Button, Frame, Menu, Scrollbar, Toplevel, NO, TOP, X, Y, W, SOLID, LEFT, RIGHT, BOTTOM, HORIZONTAL, VERTICAL

# -------- FRAMES - PRINCIPAL -----------
root = Tk()
root.title("LISTA DE PRODUTOS")
width = 800
height = 400
sc_width = root.winfo_screenwidth()
sc_height = root.winfo_screenheight()
x = (sc_width/2) - (width/2)
y = (sc_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0,0)
root.config(bg='#6666ff')


# -------- VARIAVEIS -----------

nome = StringVar()
grupo = StringVar()
preco = StringVar()
estoque = StringVar()
validade = StringVar()
id = None
janela_atualizar = None
janela_novo = None
caminho_db = 'C:\sqlite3\contatos.db'


# -------- METODOS ---------

def database():
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    query = '''CREATE TABLE IF NOT EXISTS produto (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                grupo TEXT,
                preco TEXT,
                estoque TEXT,
                validade TEXT
            )'''
    cursor.execute(query)
    cursor.execute('SELECT * FROM produto ORDER BY nome')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    cursor.close()
    conn.close()

def enviar_dados():
    if nome.get() == '' or grupo.get() == '' or preco.get() == '' or estoque.get() == '' or validade.get() == '':
        msb.showwarning('', 'Por favor, digite todos os campos.', icon='warning')
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        query = 'INSERT INTO produto (nome, grupo, preco, estoque, validade) VALUES (?, ?, ?, ?, ?)'
        cursor.execute(query, (str(nome.get()), str(grupo.get()), str(preco.get()), str(estoque.get()), str(validade.get())))
        conn.commit()
        cursor.execute('SELECT * FROM produto ORDER BY nome')
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=data)
        cursor.close()
        conn.close()
        nome.set('')
        telefone.set('')
        idade.set('')
        email.set('')
        endereco.set('')

def atualizar_dados():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    cursor.execute('''UPDATE produto SET nome = ?, grupo = ?, preco = ?, estoque = ?, validade = ? WHERE id = ?''',
                    (str(nome.get()), str(grupo.get()), str(preco.get()), str(estoque.get()), str(validade.get()), int(id)))
    conn.commit()
    cursor.execute('SELECT * FROM produto ORDER BY nome')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    cursor.close()
    conn.close()
    nome.set('')
    grupo.set('')
    preco.set('')
    estoque.set('')
    validade.set('')
    janela_atualizar.destroy()


def selecionado(event):
    global id, janela_atualizar
    item_selecionado = tree.focus()
    conteudo = (tree.item(item_selecionado))
    itens_selecionados = conteudo['values']
    id = itens_selecionados[0]
    nome.set('')
    nome.set(itens_selecionados[1])
    grupo.set('')
    grupo.set(itens_selecionados[2])
    preco.set('')
    preco.set(itens_selecionados[3])
    estoque.set('')
    estoque.set(itens_selecionados[4])
    validade.set('')
    validade.set(itens_selecionados[5])
    #------ FRAME - ATUALIZAR ---------
    janela_atualizar = Toplevel()
    janela_atualizar.title('ATUALIZAR')
    form_titulo = Frame(janela_atualizar)
    form_titulo.pack(side=TOP)
    form_contato = Frame(janela_atualizar)
    form_contato.pack(side=TOP, pady=10)
    width = 400
    height = 300
    sc_width = janela_atualizar.winfo_screenwidth()
    sc_height = janela_atualizar.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    janela_atualizar.geometry("%dx%d+%d+%d" % (width, height, x, y))
    janela_atualizar.resizable(0,0)

    #------- LABELS - ATUALIZAR -------
    lbl_titulo = Label(form_titulo, text='Atulizando produtos', font=('arial', 18), bg='BLUE', width=200)
    lbl_titulo.pack(fill=X)
    lbl_nome = Label(form_contato, text='Nome', font=('arial', 12))
    lbl_nome.grid(row=0, sticky=W)
    lbl_telefone = Label(form_contato, text='Grupo', font=('arial', 12))
    lbl_telefone.grid(row=1, sticky=W)
    lbl_idade = Label(form_contato, text='Preço', font=('arial', 12))
    lbl_idade.grid(row=2, sticky=W)
    lbl_email = Label(form_contato, text='Estoque', font=('arial', 12))
    lbl_email.grid(row=3, sticky=W)
    lbl_endereco = Label(form_contato, text='Validade', font=('arial', 12))
    lbl_endereco.grid(row=4, sticky=W)

    #-------- ENTRY - ATUALIZAR ------
    ent_nome = Entry(form_contato, textvariable=nome,  font=('arial', 12))
    ent_nome.grid(row=0, column=1)
    ent_telefone = Entry(form_contato, textvariable=grupo,  font=('arial', 12))
    ent_telefone.grid(row=1, column=1)
    ent_idade = Entry(form_contato, textvariable=preco,  font=('arial', 12))
    ent_idade.grid(row=2, column=1)
    ent_email = Entry(form_contato, textvariable=estoque,  font=('arial', 12))
    ent_email.grid(row=3, column=1)
    ent_endereco = Entry(form_contato, textvariable=validade,  font=('arial', 12))
    ent_endereco.grid(row=4, column=1)

    #------- BOTAO - ATUALIZAR ------ 
    btn_atualizar = Button(form_contato, text='Atualizar', width=50, command=atualizar_dados)
    btn_atualizar.grid(row=6, columnspan=2, pady=10)


def inserir_dado():
    global janela_novo
    nome.set('')
    grupo.set('')
    preco.set('')
    estoque.set('')
    validade.set('')

    #------ FRAME - INSERIR ---------
    janela_novo = Toplevel()
    janela_novo.title("CADASTRO")
    form_titulo = Frame(janela_novo)
    form_titulo.pack(side=TOP)
    form_contato = Frame(janela_novo)
    form_contato.pack(side=TOP, pady=10)
    width = 400
    height = 300
    sc_width = janela_novo.winfo_screenwidth()
    sc_height = janela_novo.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    janela_novo.geometry("%dx%d+%d+%d" % (width, height, x, y))
    janela_novo.resizable(0,0)

    #------- LABELS - INSERIR -------
    lbl_titulo = Label(form_titulo, text='Inserindo produtos', font=('arial', 18), bg='BLUE', width=200)
    lbl_titulo.pack(fill=X)
    lbl_nome = Label(form_contato, text='Nome', font=('arial', 12))
    lbl_nome.grid(row=0, sticky=W)
    lbl_grupo = Label(form_contato, text='Grupo', font=('arial', 12))
    lbl_grupo.grid(row=1, sticky=W)
    lbl_preco = Label(form_contato, text='Preço', font=('arial', 12))
    lbl_preco.grid(row=2, sticky=W)
    lbl_estoque = Label(form_contato, text='Estoque', font=('arial', 12))
    lbl_estoque.grid(row=3, sticky=W)
    lbl_validade = Label(form_contato, text='Validade', font=('arial', 12))
    lbl_validade.grid(row=4, sticky=W)

    #-------- ENTRY - INSERIR ------
    ent_nome = Entry(form_contato, textvariable=nome,  font=('arial', 12))
    ent_nome.grid(row=0, column=1)
    ent_telefone = Entry(form_contato, textvariable=grupo,  font=('arial', 12))
    ent_telefone.grid(row=1, column=1)
    ent_idade = Entry(form_contato, textvariable=preco,  font=('arial', 12))
    ent_idade.grid(row=2, column=1)
    ent_email = Entry(form_contato, textvariable=estoque,  font=('arial', 12))
    ent_email.grid(row=3, column=1)
    ent_endereco = Entry(form_contato, textvariable=validade,  font=('arial', 12))
    ent_endereco.grid(row=4, column=1)

    #------- BOTAO - INSERIR ------ 
    btn_atualizar = Button(form_contato, text='Cadastrar', width=50, command=enviar_dados)
    btn_atualizar.grid(row=6, columnspan=2, pady=10)


def deletar_dados():
    if not tree.selection():
        msb.showwarning('', 'Por favor, selecione um item da lista', icon='warning')
    else:
        resultado = msb.askquestion('', 'Tem certeza que deseja excluir o produto?')
        if resultado == 'yes':
            item_selecionado = tree.focus()
            conteudo = (tree.item(item_selecionado))
            item = conteudo['values']
            tree.delete(item_selecionado)
            conn = sqlite3.connect(caminho_db)
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM produto WHERE id = {item[0]}')
            conn.commit()
            cursor.close()
            conn.close()

# ------ FRAME PRINCIPAL -------------
top = Frame(root, width=500, bd=1, relief=SOLID)
top.pack(side=TOP)
mid = Frame(root, width=500, bg='#6666ff')
mid.pack(side=TOP)
midleft = Frame(mid, width=100)
midleft.pack(side=LEFT)
midleftPadding = Frame(mid, width=300, bg='#6666ff')
midleftPadding.pack(side=LEFT)
midright = Frame(mid, width=100)
midright.pack(side=RIGHT)
bottom = Frame(root, width=500)
bottom.pack(side=BOTTOM)
tableMargin = Frame(root, width=500)
tableMargin.pack(side=TOP)

# -------- LABEL PRINCIPAL -------
lbl_titulo = Label(top, text='SISTEMA DE PRODUTOS 💘 ', font=('arial', 18), width=500)
lbl_titulo.pack(fill=X)

lbl_alterar = Label(bottom, text='🚑 Para alterar, clique duas vezes no registro!', font=('arial', 18), width=500)
lbl_alterar.pack(fill=X)

# --------- BOTOES PRINCIPAL -------
bttn_incluir = Button(midleft, text='INSERIR NOVO PRODUTO', bg='white', command=inserir_dado)
bttn_incluir.pack()

bttn_excluir = Button(midright, text='EXCLUIR PRODUTO', bg='white', command=deletar_dados)
bttn_excluir.pack(side=RIGHT)

# -------- TREEVIEW PRINCIAPL ---------
ScrollbarX = Scrollbar(tableMargin, orient=HORIZONTAL)
ScrollbarY = Scrollbar(tableMargin, orient=VERTICAL)

tree = ttk.Treeview(tableMargin, columns=('ID', 'Nome', 'Grupo', 'Preço', 'Estoque', 'Validade'),
                    height=400, selectmode='extended', yscrollcommand=ScrollbarY.set, xscrollcommand=ScrollbarX.set)
ScrollbarY.config(command=tree.yview)
ScrollbarY.pack(side=RIGHT, fill=Y)
ScrollbarX.config(command=tree.xview)
ScrollbarX.pack(side=BOTTOM, fill=X)
tree.heading('ID', text='ID', anchor=W)
tree.heading('Nome', text='Nome', anchor=W)
tree.heading('Grupo', text='Grupo', anchor=W)
tree.heading('Preço', text='Preço', anchor=W)
tree.heading('Estoque', text='Estoque', anchor=W)
tree.heading('Validade', text='Validade', anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=1)
tree.column('#1', stretch=NO, minwidth=0, width=20)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=80)
tree.pack()
tree.bind('<Double-Button-1>', selecionado)

# ------ MENU - PRINCIPAL -------
menu_bar = Menu(root)
root.config(menu=menu_bar)

#adicionar itens
menu_arquivo = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Menu', menu=menu_arquivo)
menu_arquivo.add_command(label='Criar novo', command=inserir_dado)
menu_arquivo.add_separator()
menu_arquivo.add_command(label='Sair', command=root.destroy)

menu_sobre = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Sobre', menu=menu_sobre)
menu_sobre.add_command(label='Info')

if __name__ == '__main__':
    database()
    root.mainloop()