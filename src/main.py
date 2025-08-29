from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime
from .services.chatgpt_service import chatgpt_service
from .routes.questoes import CONTEUDOS_EDITAL
from .routes.signup import signup_bp
from .routes.auth import auth_bp
from .routes.questoes import questoes_bp
from .routes.planos import planos_bp
from .routes.jogos import jogos_bp
from .routes.news import news_bp
from .routes.opcoes import opcoes_bp
from .config.firebase_config import firebase_config

app = Flask(__name__)
# Configuração CORS específica para o frontend do Vercel
CORS(app, 
     origins=['https://gabarita-ai-frontend-pied.vercel.app', 'http://localhost:3000', '*'],
     allow_headers=['Content-Type', 'Authorization', 'Accept', 'Access-Control-Request-Method', 'Access-Control-Request-Headers'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     supports_credentials=True)  # Habilitar credentials para autenticação

# Registrar blueprints
app.register_blueprint(signup_bp, url_prefix='/api/auth')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(questoes_bp, url_prefix='/api/questoes')
app.register_blueprint(planos_bp, url_prefix='/api')
app.register_blueprint(jogos_bp, url_prefix='/api/jogos')
app.register_blueprint(news_bp, url_prefix='/api')
app.register_blueprint(opcoes_bp, url_prefix='/api')

@app.route('/', methods=['GET'])
def root():
    """Rota raiz da API"""
    return jsonify({
        'message': 'Gabarita.AI Backend API',
        'version': '1.0.0',
        'status': 'online',
        'endpoints': {
            'health': '/health',
            'auth': '/api/auth/*',
            'questoes': '/api/questoes/*',
            'planos': '/api/planos',
            'jogos': '/api/jogos/*',
            'opcoes': '/api/opcoes/*'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/test', methods=['GET', 'OPTIONS'])
def test_endpoint():
    """Endpoint de teste para verificar conectividade"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        return response
    
    return jsonify({
        'status': 'success',
        'message': 'API está funcionando corretamente',
        'timestamp': datetime.now().isoformat(),
        'method': request.method,
        'headers': dict(request.headers)
    })

@app.route('/api/opcoes/test', methods=['GET', 'OPTIONS'])
def test_opcoes():
    """Endpoint de teste específico para opções"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        return response
    
    opcoes_mock = {
        'opcoes_carreira': [
            {'id': 1, 'nome': 'Concursos Públicos', 'descricao': 'Preparação para concursos públicos federais, estaduais e municipais'},
            {'id': 2, 'nome': 'ENEM', 'descricao': 'Preparação completa para o Exame Nacional do Ensino Médio'},
            {'id': 3, 'nome': 'Vestibulares', 'descricao': 'Preparação para vestibulares das principais universidades'},
            {'id': 4, 'nome': 'OAB', 'descricao': 'Preparação para o Exame da Ordem dos Advogados do Brasil'},
            {'id': 5, 'nome': 'Residência Médica', 'descricao': 'Preparação para provas de residência médica'}
        ],
        'opcoes_materia': [
            {'id': 1, 'nome': 'Português', 'categoria': 'Linguagens'},
            {'id': 2, 'nome': 'Matemática', 'categoria': 'Exatas'},
            {'id': 3, 'nome': 'História', 'categoria': 'Humanas'},
            {'id': 4, 'nome': 'Geografia', 'categoria': 'Humanas'},
            {'id': 5, 'nome': 'Biologia', 'categoria': 'Natureza'},
            {'id': 6, 'nome': 'Química', 'categoria': 'Natureza'},
            {'id': 7, 'nome': 'Física', 'categoria': 'Natureza'},
            {'id': 8, 'nome': 'Direito Constitucional', 'categoria': 'Jurídica'},
            {'id': 9, 'nome': 'Direito Administrativo', 'categoria': 'Jurídica'},
            {'id': 10, 'nome': 'Informática', 'categoria': 'Tecnologia'}
        ]
    }
    
    return jsonify({
        'status': 'success',
        'data': opcoes_mock,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def api_health():
    """API Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Simulação de login para testes"""
    data = request.get_json()
    
    # Simulação simples de autenticação
    return jsonify({
        'success': True,
        'message': 'Login realizado com sucesso',
        'user': {
            'id': '123',
            'email': data.get('email', 'test@example.com'),
            'name': 'Usuário Teste'
        },
        'token': 'mock_jwt_token_123'
    })

@app.route('/api/questoes/gerar', methods=['POST'])
def gerar_questao_endpoint():
    """Endpoint para gerar questões com fallback"""
    try:
        data = request.get_json()
        materia = data.get('materia', 'Português')
        dificuldade = data.get('dificuldade', 'medio')
        quantidade = data.get('quantidade', 1)
        
        # Tentar usar o serviço ChatGPT primeiro
        try:
            questoes = chatgpt_service.gerar_questoes(
                materia=materia,
                dificuldade=dificuldade,
                quantidade=quantidade
            )
            
            if questoes:
                return jsonify({
                    'success': True,
                    'questoes': questoes,
                    'fonte': 'chatgpt',
                    'message': f'{len(questoes)} questão(ões) gerada(s) com sucesso'
                })
        except Exception as e:
            print(f"Erro no ChatGPT: {e}")
        
        # Fallback: questões estáticas baseadas na matéria
        questoes_fallback = [
            {
                'id': f'q_{i+1}',
                'enunciado': f'Questão de {materia} - Nível {dificuldade.title()}. Esta é uma questão de exemplo para testar a funcionalidade do sistema.',
                'alternativas': [
                    {'letra': 'A', 'texto': 'Primeira alternativa'},
                    {'letra': 'B', 'texto': 'Segunda alternativa'},
                    {'letra': 'C', 'texto': 'Terceira alternativa'},
                    {'letra': 'D', 'texto': 'Quarta alternativa'},
                    {'letra': 'E', 'texto': 'Quinta alternativa'}
                ],
                'resposta_correta': 'A',
                'explicacao': f'Esta é a explicação da questão de {materia}.',
                'materia': materia,
                'dificuldade': dificuldade,
                'tags': [materia.lower(), dificuldade]
            } for i in range(quantidade)
        ]
        
        return jsonify({
            'success': True,
            'questoes': questoes_fallback,
            'fonte': 'fallback',
            'message': f'{len(questoes_fallback)} questão(ões) gerada(s) com sucesso (modo fallback)'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro ao gerar questões'
        }), 500

@app.route('/api/questoes/<questao_id>/responder', methods=['POST'])
def responder_questao(questao_id):
    """Endpoint para responder questões"""
    data = request.get_json()
    resposta = data.get('resposta')
    
    # Simulação de verificação de resposta
    return jsonify({
        'success': True,
        'correto': resposta == 'A',  # Simulação
        'resposta_correta': 'A',
        'explicacao': 'Esta é uma explicação simulada da resposta correta.'
    })

@app.route('/api/perplexity/explicacao', methods=['POST'])
def obter_explicacao_perplexity():
    """Endpoint para obter explicações com fallback"""
    try:
        data = request.get_json()
        questao = data.get('questao', '')
        resposta = data.get('resposta', '')
        
        # Tentar usar serviço real primeiro (implementar depois)
        # Por enquanto, usar fallback
        
        explicacao_fallback = f"""
        **Explicação da Questão:**
        
        A questão aborda conceitos fundamentais da matéria em questão. 
        
        **Análise das Alternativas:**
        
        - **Alternativa A**: Esta é a resposta correta porque...
        - **Alternativa B**: Incorreta, pois...
        - **Alternativa C**: Não se aplica porque...
        - **Alternativa D**: Embora pareça correta, está errada devido a...
        - **Alternativa E**: Claramente incorreta, já que...
        
        **Dica de Estudo:**
        Para dominar este tipo de questão, é importante revisar os conceitos básicos e praticar com exercícios similares.
        
        **Resposta Selecionada:** {resposta}
        
        Esta explicação foi gerada automaticamente pelo sistema Gabarita.AI.
        """
        
        return jsonify({
            'success': True,
            'explicacao': explicacao_fallback,
            'fonte': 'fallback',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro ao obter explicação'
        }), 500

@app.route('/api/simulados/submit', methods=['POST'])
def submit_simulado():
    """Endpoint para submeter simulados e calcular score"""
    try:
        data = request.get_json()
        respostas = data.get('respostas', [])
        tempo_total = data.get('tempo_total', 0)
        
        # Simulação de cálculo de score
        total_questoes = len(respostas)
        acertos = sum(1 for r in respostas if r.get('correta', False))
        percentual = (acertos / total_questoes * 100) if total_questoes > 0 else 0
        
        # Determinar desempenho
        if percentual >= 80:
            desempenho = 'Excelente'
        elif percentual >= 60:
            desempenho = 'Bom'
        elif percentual >= 40:
            desempenho = 'Regular'
        else:
            desempenho = 'Precisa Melhorar'
        
        return jsonify({
            'success': True,
            'resultado': {
                'total_questoes': total_questoes,
                'acertos': acertos,
                'erros': total_questoes - acertos,
                'percentual': round(percentual, 2),
                'desempenho': desempenho,
                'tempo_total': tempo_total,
                'tempo_medio_questao': round(tempo_total / total_questoes, 2) if total_questoes > 0 else 0
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro ao processar simulado'
        }), 500

@app.route('/api/performance', methods=['GET'])
def get_performance():
    """Endpoint para obter dados de performance (simulado)"""
    # Dados simulados de performance
    performance_data = {
        'resumo': {
            'total_simulados': 15,
            'media_acertos': 75.5,
            'melhor_performance': 92.0,
            'tempo_total_estudos': 2450  # em minutos
        },
        'historico_semanal': [
            {'semana': '2024-01', 'acertos': 70, 'simulados': 3},
            {'semana': '2024-02', 'acertos': 75, 'simulados': 4},
            {'semana': '2024-03', 'acertos': 80, 'simulados': 5},
            {'semana': '2024-04', 'acertos': 78, 'simulados': 3}
        ],
        'materias': [
            {'nome': 'Português', 'acertos': 85, 'total': 100},
            {'nome': 'Matemática', 'acertos': 70, 'total': 100},
            {'nome': 'História', 'acertos': 75, 'total': 80},
            {'nome': 'Geografia', 'acertos': 80, 'total': 90}
        ]
    }
    
    return jsonify({
        'success': True,
        'data': performance_data,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/ranking', methods=['GET'])
def get_ranking():
    """Endpoint para obter dados de ranking (simulado)"""
    # Dados simulados de ranking
    ranking_data = {
        'posicao_usuario': 15,
        'total_usuarios': 1250,
        'percentil': 88.0,
        'top_10': [
            {'posicao': 1, 'nome': 'Ana Silva', 'pontos': 2450, 'avatar': None},
            {'posicao': 2, 'nome': 'João Santos', 'pontos': 2380, 'avatar': None},
            {'posicao': 3, 'nome': 'Maria Oliveira', 'pontos': 2320, 'avatar': None}
        ]
    }
    
    return jsonify({
        'success': True,
        'data': ranking_data,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)