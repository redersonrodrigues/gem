.. GEM documentation master file, created by
   sphinx-quickstart on Fri Jun 13 21:27:18 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GEM - Gestão de Escalas Médicas
===============================

Bem-vindo à documentação técnica do GEM!

.. contents:: Sumário
   :depth: 2
   :local:

Visão Geral
-----------
O GEM é um sistema para gestão de escalas médicas, cadastro de profissionais, especializações e relatórios, desenvolvido em Python com Flask, SQLite, SQLAlchemy, Bootstrap e PyQt5.

.. image:: _static/fluxo_gem.png
   :alt: Fluxograma do GEM
   :align: center

Exemplo de Uso
--------------

.. code-block:: python

   from app.models.doctor import Doctor
   from app.models.specialization import Specialization
   # Criar um médico com especializações
   cardiologia = Specialization(name="CARDIOLOGIA")
   medico = Doctor(name="JOÃO DA SILVA", fantasy_name="CLÍNICA SILVA")
   medico.specializations.append(cardiologia)

.. toctree::
   :maxdepth: 2
   :caption: Conteúdo

   modules

