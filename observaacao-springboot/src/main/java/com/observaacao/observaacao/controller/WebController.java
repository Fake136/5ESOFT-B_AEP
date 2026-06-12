package com.observaacao.observaacao.controller;

import com.observaacao.observaacao.model.Solicitacao;
import com.observaacao.observaacao.service.SolicitacaoService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@Controller
public class WebController {

    private final SolicitacaoService service;

    public WebController(SolicitacaoService service) {
        this.service = service;
    }

    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("title", "Home");
        return "pages/home";
    }

    @GetMapping("/cadastro")
    public String cadastroForm(Model model) {
        model.addAttribute("solicitacao", new Solicitacao());
        model.addAttribute("title", "Nova Solicitação");
        return "pages/cadastro";
    }

    @PostMapping("/cadastro")
    public String salvarSolicitacao(@ModelAttribute Solicitacao solicitacao, Model model) {
        Solicitacao salva = service.criarSolicitacao(solicitacao);
        model.addAttribute("solicitacao", salva);
        model.addAttribute("title", "Confirmação");
        return "pages/confirmacao";
    }

    @GetMapping("/busca")
    public String buscaForm(@RequestParam(required = false) String protocolo, Model model) {
        if (protocolo != null && !protocolo.isEmpty()) {
            service.buscarPorProtocolo(protocolo).ifPresent(s -> model.addAttribute("solicitacao", s));
        }
        model.addAttribute("title", "Acompanhar Protocolo");
        return "pages/busca-protocolo";
    }

    @GetMapping("/gestor/demandas")
    public String listaDemandas(Model model) {
        model.addAttribute("solicitacoes", service.listarTodas());
        model.addAttribute("title", "Painel do Gestor");
        return "pages/lista-demandas";
    }

    @GetMapping("/gestor/detalhes/{id}")
    public String detalhesSolicitacao(@PathVariable UUID id, Model model) {
        service.buscarPorId(id).ifPresent(s -> {  // Vamos precisar criar este método no Service
            model.addAttribute("solicitacao", s);
        });
        model.addAttribute("title", "Detalhes da Solicitação");
        return "pages/detalhes-solicitacao";
    }
    @PostMapping("/gestor/atualizar/{id}")
    public String atualizarStatus(@PathVariable UUID id,
                                  @RequestParam String status,
                                  @RequestParam String comentario,
                                  @RequestParam String responsavel,
                                  Model model) {

        Solicitacao atualizada = service.atualizarStatus(id, status, comentario, responsavel);
        model.addAttribute("solicitacao", atualizada);
        return "pages/detalhes-solicitacao";
    }
}