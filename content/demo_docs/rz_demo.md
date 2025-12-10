
# Rechenzentrum – Gesamtübersicht

Dieses Dokument beschreibt die Gesamtarchitektur unseres Rechenzentrums.

## Ziele

- Hohe Verfügbarkeit der Kernsysteme
- Klare Trennung von Zonen (DMZ, Applikationszone, Datenzone)
- Nutzung von Kubernetes für containerisierte Workloads
- Integration eines lokalen RAG-Systems (Ollama + Chroma)

## Komponenten

- **Core-Switches** zur Vernetzung der RZ-Racks
- **Firewall-Cluster** zur Segmentierung und Absicherung
- **Virtualisierungs-Cluster** (z. B. VMware / KVM / Proxmox)
- **Kubernetes-Cluster** für moderne Anwendungen
- **Storage-System** für VMs, Container-Volumes und Backups
- **Backup-System** für tägliche/monatliche Sicherungen

## RAG-Demo-System

Das RAG-Demo-System besteht aus:
- einem lokalen LLM (Ollama, z. B. `llama3:8b`)
- einer Vektordatenbank (Chroma)
- einer FastAPI-Anwendung (`rag-api`) mit Web-UI

Es läuft im Kubernetes-Cluster und dient als Demo für:
- Wissensabfragen zu Architektur- und Betriebsdokumentation
- Prototyp für zukünftige Wissensmanagement-Lösungen im RZ.
EOF
