from django.shortcuts import render, HttpResponseRedirect
from caixas.models import Conta
from django.db.models import Q
from pessoas.models import Pessoa

def index(request):
    return render(request, 'index.html')

def contaListar(request):
    contas = Conta.objects.all()[0:10]
    #TESTE LOCAL PARA VERIFICAR SE A TABELA ESTA LISTANDO
    #contas = []
    #contas.append(Conta(tipo='E', descricao='MAIL', pessoa_id=1 ))
    return render(request, 'caixas/listaContas.html', {'contas': contas})

def contaAdicionar(request):
    return render(request, 'caixas/formContas.html')

def contaSalvar(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '0')

        try:
            conta = Conta.objects.get(pk=codigo)
        except:
            conta = Conta()
        conta.pessoa_id = 1    
        conta.tipo = request.POST.get('tipo', '').upper()
        conta.descricao = request.POST.get('descricao', '').upper()
        conta.valor = request.POST.get('valor', '').upper()
        conta.pagseguro = request.POST.get('pagseguro', '').upper()
        conta.data = request.POST.get('data', '').upper()

        conta.save()
        return HttpResponseRedirect('/caixas/')

def contaPesquisar(request):
    if request.method == 'POST':
        textoBusca = request.POST.get('textoBusca', 'TUDO').upper()
        try:
            if textoBusca == 'TUDO':
                contas = Conta.objects.all()
            else: 
                contas = Conta.objects.filter(
                    (Q(tipo__contains=textoBusca) |  
                    Q(descricao__contains=textoBusca) | 
                    Q(valor__contains=textoBusca) |
                    Q(pagseguro__contains=textoBusca) |
                    Q(pagseguro__contains=textoBusca))).order_by('-descricao')  
        except:
            contas = []

        return render(request, 'caixas/listaContas.html', {'contas': contas, 'textoBusca': textoBusca})

def contaEditar(request, pk=0):
    try:
        conta = Conta.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/caixas/')

    return render(request, 'caixas/formContas.html', {'conta': conta})

def contaExcluir(request, pk=0):
    try:
        conta = Conta.objects.get(pk=pk)
        conta.delete()
        return HttpResponseRedirect('/caixas/')
    except:
        return HttpResponseRedirect('/caixas/')