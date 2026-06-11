package com.observaacao.observaacao.model;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Data
public class HistoricoStatus {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String statusAnterior;
    private String novoStatus;
    private String comentario;
    private String responsavel;
    private LocalDateTime data = LocalDateTime.now();
}