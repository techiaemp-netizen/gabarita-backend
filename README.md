# Gabarita AI - Backend

Backend do sistema Gabarita AI - Plataforma de simulados e estudos preparatórios com inteligência artificial.

## Tecnologias

- **Framework**: Flask
- **Banco de Dados**: SQLAlchemy
- **Autenticação**: Firebase Auth
- **Pagamentos**: Mercado Pago
- **IA**: OpenAI GPT
- **Deploy**: Render

## Funcionalidades

- Sistema de autenticação completo
- Gestão de usuários e planos
- Geração de questões com IA
- Sistema de simulados
- Dashboard de desempenho
- Integração com Mercado Pago
- Sistema de ranking
- Redação com correção automática
- Notícias e conteúdo educacional

## Deploy

Este projeto está configurado para deploy automático no Render usando o arquivo `render.yaml`.

## Variáveis de Ambiente

- `PORT`: Porta do servidor (padrão: 5000)
- `PYTHON_VERSION`: Versão do Python (3.11.0)
- `OPENAI_API_KEY`: Chave da API OpenAI
- `FIREBASE_*`: Configurações do Firebase
- `MERCADO_PAGO_*`: Configurações do Mercado Pago

## Estrutura

```
src/
├── main.py              # Aplicação principal
├── config/              # Configurações
├── models/              # Modelos de dados
├── routes/              # Rotas da API
├── services/            # Serviços externos
└── utils/               # Utilitários
```

## Endpoints Principais

- `GET /health` - Health check
- `POST /auth/login` - Login
- `POST /auth/signup` - Cadastro
- `GET /api/user/profile` - Perfil do usuário
- `GET /api/planos` - Planos disponíveis
- `POST /api/questoes/gerar` - Gerar questões
- `POST /api/simulados` - Criar simulado
- `GET /api/dashboard` - Dashboard
- `POST /api/payments/create` - Criar pagamento

---

© 2024 Gabarita AI. Todos os direitos reservados.