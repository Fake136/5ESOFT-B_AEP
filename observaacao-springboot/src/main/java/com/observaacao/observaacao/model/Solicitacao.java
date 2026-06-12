package com.observaacao.observaacao.model;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Data
public class Solicitacao {

    @Id
    private UUID id;

    private String protocolo;

    private String categoria;
    private String descricao;
    private String localizacao;
    private String prioridade;
    private boolean anonimo;

    private String nomeCidadao;
    private String contato;

    private String status = "ABERTO";

    private LocalDateTime dataCriacao = LocalDateTime.now();

    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    private List<HistoricoStatus> historico = new ArrayList<>();


    public Solicitacao() {
        this.id = UUID.randomUUID();
    }


    public void gerarProtocolo() {
        if (this.protocolo == null) {
            this.protocolo = "PROTO-" + this.id.toString().substring(0, 8).toUpperCase();
        }
    }
}