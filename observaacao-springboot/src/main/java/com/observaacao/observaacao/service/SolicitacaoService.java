package com.observaacao.observaacao.service;

import com.observaacao.observaacao.model.Solicitacao;
import com.observaacao.observaacao.model.HistoricoStatus;
import com.observaacao.observaacao.repository.SolicitacaoRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class SolicitacaoService {

    private final SolicitacaoRepository repository;

    public SolicitacaoService(SolicitacaoRepository repository) {
        this.repository = repository;
    }

    public Solicitacao criarSolicitacao(Solicitacao solicitacao) {
        if (solicitacao.isAnonimo()) {
            solicitacao.setNomeCidadao(null);
            solicitacao.setContato(null);
        }
        return repository.save(solicitacao);
    }

    public Optional<Solicitacao> buscarPorProtocolo(String protocolo) {
        return repository.findByProtocolo(protocolo);
    }

    public Optional<Solicitacao> buscarPorId(UUID id) {
        return repository.findById(id);
    }

    public List<Solicitacao> listarTodas() {
        return repository.findAll();
    }

    public Solicitacao atualizarStatus(UUID id, String novoStatus, String comentario, String responsavel) {
        Solicitacao s = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Solicitação não encontrada: " + id));

        HistoricoStatus historico = new HistoricoStatus();
        historico.setStatusAnterior(s.getStatus());
        historico.setNovoStatus(novoStatus);
        historico.setComentario(comentario);
        historico.setResponsavel(responsavel);

        s.getHistorico().add(historico);
        s.setStatus(novoStatus);

        return repository.save(s);
    }
}