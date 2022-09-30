from flask import render_template, flash, redirect, url_for, request
from Estoque import app, database                                 #, database, bcrypt
from Estoque.forms import Form_login, Form_adc, Form_rem, Form_qtd, Form_proc, Form_edt
from Estoque. models import Usuarios, Itens, Historico
from flask_login import login_user, logout_user, current_user, login_required

#from nomedapasta.models import tabelas...
#from flask_login import login_user, logout_user, current_user, login_required

@app.route('/', methods=['GET', 'POST'])
def logar():
   form_login = Form_login()
   if form_login.validate_on_submit():
      usuario = Usuarios.query.filter_by(nome=form_login.usuario.data).first()
      if usuario and usuario.senha == form_login.senha.data:
         login_user(usuario, remember=False)
         flash('Ação Realizada Com Sucesso!', 'alert-success')
         return redirect(url_for('inicio'))
      else:
         flash('Deu ruim', 'alert-danger')

   return render_template('logar.html', form_login=form_login)


@app.route('/home')
@login_required
def inicio():
   itens = Itens.query.all()

   return render_template('home.html', itens=itens)

@app.route('/adicionar', methods=['GET', 'POST'])
@login_required
def adc():
   form_adc = Form_adc()
   if form_adc.validate_on_submit():
      cod = form_adc.cod.data
      nome = form_adc.nome.data
      lote = form_adc.lote.data
      qtd = form_adc.qtd.data
      form_adc.cod.data = ''
      form_adc.nome.data = ''
      form_adc.lote.data = ''
      form_adc.qtd.data = ''
      if Itens.query.filter_by(cod_item=cod, lote_item=lote).first():
         flash('Item já existente!', 'alert-danger')
      else:
         item = Itens(cod_item=cod, nome_item=nome, lote_item=lote, quantidade_item=qtd)
         database.session.add(item)
         database.session.commit()
         id = Itens.query.filter_by(cod_item=cod, lote_item=lote).first()
         registro = Historico(id_item=id.id_item, usuario=current_user.nome, acao='Item Criado', cod_item='-',
                              cod_item_ed=cod, nome_item='-', nome_item_ed=nome, lote_item='-', lote_item_ed=lote,
                              quantidade_item=0, quantidade_item_ed=qtd)
         database.session.add(registro)
         database.session.commit()
         flash('Item Adicionado Com Sucesso!', 'alert-success')

   return render_template('criar.html', form_adc=form_adc)

@app.route('/remover', methods=['GET', 'POST'])
@login_required
def rem():
   form_rem = Form_rem()
   if form_rem.validate_on_submit():
      item = Itens.query.filter_by(cod_item=form_rem.cod.data, lote_item=form_rem.lote.data).first()
      if item:
         cod = item.cod_item
         nome = item.nome_item
         lote = item.lote_item
         qtd = item.quantidade_item
         database.session.delete(item)
         database.session.commit()
         registro = Historico(id_item=item.id_item, usuario=current_user.nome, acao='Item deletado', cod_item=cod,
                              cod_item_ed='-', nome_item=nome, nome_item_ed='-', lote_item=lote, lote_item_ed='-',
                              quantidade_item=qtd, quantidade_item_ed=0)
         database.session.add(registro)
         database.session.commit()
         flash('Item Removido Com Sucesso!', 'alert-success')
      else:
         flash('Item Não Encontrado!', 'alert-danger')

   return render_template('remover.html', form_rem=form_rem)

@app.route('/qtde',  methods=['GET', 'POST'])
@login_required
def qtd():
   form_qtd = Form_qtd()
   if form_qtd.validate_on_submit():
      item = Itens.query.filter_by(cod_item=form_qtd.cod.data, lote_item=form_qtd.lote.data).first()
      if item:
         cod = item.cod_item
         nome = item.nome_item
         lote = item.lote_item
         qtd = item.quantidade_item
         qtdn = form_qtd.qtd.data
         if form_qtd.opcao.data == 'Adicionar':
            item.quantidade_item += form_qtd.qtd.data
            database.session.commit()
            registro = Historico(id_item=item.id_item, usuario=current_user.nome, acao='Adicionando qtde', cod_item=cod,
                                 cod_item_ed='-', nome_item=nome, nome_item_ed='-', lote_item=lote, lote_item_ed='-',
                                 quantidade_item=qtd, quantidade_item_ed=qtd+qtdn)
            database.session.add(registro)
            database.session.commit()
            flash('Adição Realizada Com Sucesso!', 'alert-success')
         else:
            if qtd >= qtdn:
               item.quantidade_item -= form_qtd.qtd.data
               database.session.commit()
               registro = Historico(id_item=item.id_item, usuario=current_user.nome, acao='Removendo qtde', cod_item=cod,
                                    cod_item_ed='-', nome_item=nome, nome_item_ed='-', lote_item=lote, lote_item_ed='-',
                                    quantidade_item=qtd, quantidade_item_ed=qtd-qtdn)
               database.session.add(registro)
               database.session.commit()
               flash('Redução Realizada Com Sucesso!', 'alert-success')
            else:
               flash('Você está tentando reduzir uma quantidade maior que a disponível no estoque!', 'alert-danger')
      else:
         flash('Item Não Encontrado!', 'alert-danger')


   return render_template('qtd.html', form_qtd=form_qtd)

@app.route('/procurar', methods=['GET', 'POST'])
@login_required
def proc():
   i = 0
   itens = None
   historico = None
   form_proc = Form_proc()
   if form_proc.validate_on_submit():
      itens = Itens.query.filter_by(cod_item=form_proc.cod.data).all()
      lista_ids = []
      for item in itens:
         lista_ids.append(item.id_item)
      historico = []
      for id in lista_ids:
         historico.append(Historico.query.filter_by(id_item=id).all())
      if len(itens) > 0:
         i = 1
         flash('Busca Realizada Com Sucesso!', 'alert-success')
      else:
         i = 0
         flash('Item Não Encontrado!', 'alert-danger')
   return render_template('procurar.html', form_proc=form_proc, i=i, itens=itens, historico=historico)

@app.route('/editar/<item_id>', methods=['GET', 'POST'])
@login_required
def editar_item(item_id):
   item = Itens.query.get(item_id)
   historico = Historico.query.filter_by(id_item = item_id).all()
   cod = item.cod_item
   nome = item.nome_item
   lote = item.lote_item
   qtd = item.quantidade_item
   form_edt = Form_edt()
   if request.method == 'GET':
      form_edt.cod.data = cod
      form_edt.nome.data = nome
      form_edt.lote.data = lote

   if form_edt.validate_on_submit() and 'confirmar' in request.form:
      if Itens.query.filter_by(cod_item=form_edt.cod.data, lote_item=form_edt.lote.data).first():
         flash('Você está tentando realizar edições alterando os dados atuais para dados de algum item já existente!', 'alert-danger')
      else:
         item.cod_item = form_edt.cod.data
         item.nome_item = form_edt.nome.data
         item.lote_item = form_edt.lote.data
         database.session.commit()

         if item.cod_item != cod:
            registro = Historico(id_item=item.id_item, usuario=current_user.nome, acao='Código editado', cod_item=cod,
                                 cod_item_ed=item.cod_item, nome_item=nome, nome_item_ed='-', lote_item=lote, lote_item_ed='-',
                                 quantidade_item=qtd, quantidade_item_ed=qtd)
            database.session.add(registro)
            database.session.commit()

         if item.nome_item != nome:
            registro = Historico(id_item=item.id_item, usuario=current_user.nome, acao='Nome editado', cod_item=cod,
                                 cod_item_ed='-', nome_item=nome, nome_item_ed=item.nome_item, lote_item=lote, lote_item_ed='-',
                                 quantidade_item=qtd, quantidade_item_ed=qtd)
            database.session.add(registro)
            database.session.commit()

         if item.lote_item != lote:
            registro = Historico(id_item=item.id_item, usuario=current_user.nome, acao='Lote editado', cod_item=cod,
                                 cod_item_ed='-', nome_item=nome, nome_item_ed='-', lote_item=lote, lote_item_ed=item.lote_item,
                                 quantidade_item=qtd, quantidade_item_ed=qtd)
            database.session.add(registro)
            database.session.commit()

         flash('Edição Realizada com Sucesso!', 'alert-success')

   if form_edt.validate_on_submit() and 'cancelar' in request.form:
      return redirect(url_for('inicio'))

   return render_template('editar_item.html', produto=item, form_edt=form_edt, historico=historico)

@app.route('/sair')
@login_required
def sair():
   logout_user()
   flash('Logout realizado com sucesso!', 'alert-success')
   return redirect(url_for('logar'))


