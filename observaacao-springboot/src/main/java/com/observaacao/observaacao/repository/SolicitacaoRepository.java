package com.observaacao.observaacao.repository;

import com.observaacao.observaacao.model.Solicitacao;
import org.springframework.stereotype.Repository;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class SolicitacaoRepository {

    private final Map<UUID, Solicitacao> solicitacoes = new ConcurrentHashMap<>();

    public Solicitacao save(Solicitacao s) {
        if (s.getId() == null) {
            s.setId(UUID.randomUUID());
        }
        s.gerarProtocolo();                    // Gera o protocolo
        solicitacoes.put(s.getId(), s);
        return s;
    }

    public Optional<Solicitacao> findById(UUID id) {
        return Optional.ofNullable(solicitacoes.get(id));
    }

    public Optional<Solicitacao> findByProtocolo(String protocolo) {
        return solicitacoes.values().stream()
                .filter(s -> s.getProtocolo().equals(protocolo))
                .findFirst();
    }

    public List<Solicitacao> findAll() {
        return new ArrayList<>(solicitacoes.values());
    }
}