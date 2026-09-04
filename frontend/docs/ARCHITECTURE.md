# HerVoice AI — Architecture

## Overview

HerVoice AI is a privacy-focused conversational support platform designed
to provide supportive conversation, information, verified resources,
and practical decision support.

The system is designed around anonymous browser sessions rather than
mandatory identity-based accounts.

## High-Level Architecture

React + TypeScript + Vite
        |
        | POST /api/chat
        v
FastAPI Backend
        |
        +-------------------+
        |                   |
        v                   v
Safety Detection       SQLite
        |                   |
        v                   |
Emotion / Intent            |
        |                   |
        +---------+---------+
                  |
                  v
          Knowledge Retrieval
                  |
                  v
          Verified Resources
                  |
                  v
               Groq
                  |
                  v
          Structured Response
                  |
                  v
              React UI

## Anonymous Sessions

HerVoice does not require a name, email address, or password.

A random browser-generated session identifier is stored locally and
used to associate conversations with the anonymous browser session.

This provides continuity while minimizing identity collection.

## Conversation Persistence

Conversation messages are stored in SQLite.

A session can be restored using:

GET /api/sessions/{session_id}

## Safety

The backend checks incoming messages through a dedicated safety detector
before normal AI generation.

Safety-related responses are routed through the safety response layer.

## Resource Grounding

Verified resources are stored in a structured knowledge dataset.

The retrieval layer only supplies resources when the query has relevant
matches.

The model is instructed not to invent organizations, phone numbers,
laws, or other resources.

## AI Provider

Groq provides the conversational language model through an
OpenAI-compatible API interface.

## Limitations

The system is not a therapist, doctor, lawyer, emergency service,
or replacement for qualified professional support.

Anonymous browser sessions are not equivalent to guaranteed anonymity
from infrastructure or hosting providers.

SQLite is suitable for the current prototype/deployment stage but a
managed production database should be considered for a larger deployment.