package com.observaacao.observaacao.controller;

import com.observaacao.observaacao.model.Solicitacao;
import com.observaacao.observaacao.service.SolicitacaoService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/solicitacoes")
@CrossOrigin(origins = "*")  // facilita testes
public class SolicitacaoController {

    private final SolicitacaoService service;

    public SolicitacaoController(SolicitacaoService service) {
        this.service = service;
    }

    // Criar solicitação
    @PostMapping
    public ResponseEntity<Solicitacao> criar(@RequestBody Solicitacao solicitacao) {
        return ResponseEntity.ok(service.criarSolicitacao(solicitacao));
    }

    // Buscar por protocolo
    @GetMapping("/protocolo/{protocolo}")
    public ResponseEntity<Solicitacao> buscarPorProtocolo(@PathVariable String protocolo) {
        return service.buscarPorProtocolo(protocolo)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // Listar todas
    @GetMapping
    public List<Solicitacao> listarTodas() {
        return service.listarTodas();
    }

    // Atualizar status
    @PutMapping("/{id}/status")
    public ResponseEntity<Solicitacao> atualizarStatus(
            @PathVariable UUID id,
            @RequestParam String status,
            @RequestParam String comentario,
            @RequestParam String responsavel) {

        return ResponseEntity.ok(service.atualizarStatus(id, status, comentario, responsavel));
    }
}