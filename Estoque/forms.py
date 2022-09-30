from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, ValidationError

class Form_login(FlaskForm):
    usuario = StringField('Usuário:', validators=[DataRequired()])
    senha = PasswordField('Senha:', validators=[DataRequired()])
    logar = SubmitField("Confirmar")

class Form_adc(FlaskForm):
    cod = StringField('Código:', validators=[DataRequired(), Length(5,10)])
    nome = StringField('Nome:', validators=[DataRequired()])
    lote = StringField('Lote:', validators=[DataRequired()])
    qtd = IntegerField('Quantidade:', validators=[DataRequired()])
    confirmar = SubmitField("Confirmar")

class Form_rem(FlaskForm):
    cod = StringField('Código:', validators=[DataRequired(), Length(5,10)])
    lote = StringField('Lote:', validators=[DataRequired()])
    confirmar = SubmitField("Confirmar")

class Form_qtd(FlaskForm):
    cod = StringField('Código:', validators=[DataRequired(), Length(5,10)])
    lote = StringField('Lote:', validators=[DataRequired()])
    qtd = IntegerField('Quantidade:', validators=[DataRequired()])
    opcao = RadioField(choices=[('Adicionar','Adicionar'), ('Remover', 'Remover')], coerce=str, validators=[DataRequired()])
    confirmar = SubmitField("Confirmar")

class Form_proc(FlaskForm):
    cod = StringField('Código:', validators=[DataRequired()])
    confirmar = SubmitField("Confirmar")

class Form_edt(FlaskForm):
    cod = StringField('Código:', validators=[DataRequired(), Length(5,10)])
    nome = StringField('Nome:', validators=[DataRequired()])
    lote = StringField('Lote:', validators=[DataRequired()])
    confirmar = SubmitField("Confirmar")
    cancelar = SubmitField("Cancelar")