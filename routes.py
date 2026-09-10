from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Veiculo, Motorista, Mecanico, Peca, Manutencao, ItemManutencao

main = Blueprint('main', __name__)

# --- 1. CRUD VEÍCULOS ---
@main.route('/veiculos', methods=['GET', 'POST'])
def listar_veiculos():
    if request.method == 'POST':
        placa = request.form.get('placa')
        modelo = request.form.get('modelo')
        ano = request.form.get('ano')
        km = request.form.get('quilometragem')

        novo_veiculo = Veiculo(placa=placa, modelo=modelo, ano=int(ano), quilometragem=int(km))
        db.session.add(novo_veiculo)
        db.session.commit()
        return redirect(url_for('main.listar_veiculos'))

    veiculos = Veiculo.query.all()
    return render_template('veiculos.html', veiculos=veiculos)

@main.route('/veiculos/excluir/<int:id>')
def excluir_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    db.session.delete(veiculo)
    db.session.commit()
    return redirect(url_for('main.listar_veiculos'))

# --- 2. CRUD MOTORISTAS ---
@main.route('/motoristas', methods=['GET', 'POST'])
def listar_motoristas():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cnh = request.form.get('cnh')
        categoria = request.form.get('categoria_cnh')
        telefone = request.form.get('telefone')

        novo_motorista = Motorista(nome=nome, cnh=cnh, categoria_cnh=categoria, telefone=telefone)
        db.session.add(novo_motorista)
        db.session.commit()
        return redirect(url_for('main.listar_motoristas'))

    motoristas = Motorista.query.all()
    return render_template('motoristas.html', motoristas=motoristas)

# --- 3. CRUD PEÇAS / ESTOQUE ---
@main.route('/pecas', methods=['GET', 'POST'])
def listar_pecas():
    if request.method == 'POST':
        nome = request.form.get('nome')
        fabricante = request.form.get('fabricante')
        valor = float(request.form.get('valor'))
        qtd = int(request.form.get('qtd_estoque'))
        minimo = int(request.form.get('estoque_minimo'))

        nova_peca = Peca(nome=nome, fabricante=fabricante, valor=valor, qtd_estoque=qtd, estoque_minimo=minimo)
        db.session.add(nova_peca)
        db.session.commit()
        return redirect(url_for('main.listar_pecas'))

    pecas = Peca.query.all()
    return render_template('pecas.html', pecas=pecas)

# --- 4. MANUTENÇÃO (REGISTRO) ---
@main.route('/manutencao/nova', methods=['GET', 'POST'])
def nova_manutencao():
    if request.method == 'POST':
        id_veiculo = int(request.form.get('id_veiculo'))
        id_mecanico = int(request.form.get('id_mecanico'))
        tipo = request.form.get('tipo')
        descricao = request.form.get('descricao')

        manutencao = Manutencao(
            id_veiculo=id_veiculo,
            id_mecanico=id_mecanico,
            tipo=tipo,
            descricao=descricao
        )
        db.session.add(manutencao)
        db.session.flush()

        id_peca = request.form.get('id_peca')
        qtd_peca = request.form.get('quantidade_peca')

        if id_peca and qtd_peca and int(qtd_peca) > 0:
            peca = Peca.query.get(int(id_peca))
            qtd = int(qtd_peca)

            if peca and peca.qtd_estoque >= qtd:
                item = ItemManutencao(
                    id_manutencao=manutencao.id_manutencao,
                    id_peca=peca.id_peca,
                    quantidade=qtd,
                    valor_unitario=peca.valor
                )
                peca.qtd_estoque -= qtd
                db.session.add(item)

        db.session.commit()
        return redirect(url_for('main.listar_veiculos'))

    veiculos = Veiculo.query.all()
    mecanicos = Mecanico.query.all()
    pecas = Peca.query.all()
    return render_template('manutencao_form.html', veiculos=veiculos, mecanicos=mecanicos, pecas=pecas)

# --- 5. RELATÓRIOS ---
@main.route('/relatorio/historico', methods=['GET'])
def relatorio_historico():
    placa = request.args.get('placa')
    veiculo = None
    manutencoes = []

    if placa:
        veiculo = Veiculo.query.filter_by(placa=placa).first()
        if veiculo:
            manutencoes = Manutencao.query.filter_by(id_veiculo=veiculo.id_veiculo).all()

    return render_template('relatorio_historico.html', veiculo=veiculo, manutencoes=manutencoes)

@main.route('/relatorio/estoque-critico')
def relatorio_estoque():
    pecas_criticas = Peca.query.filter(Peca.qtd_estoque <= Peca.estoque_minimo).all()
    return render_template('relatorio_estoque.html', pecas=pecas_criticas)