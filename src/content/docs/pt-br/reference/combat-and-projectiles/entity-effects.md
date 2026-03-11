---
title: Efeitos de Entidade
description: Referencia para definicoes de efeitos de entidade no lado do servidor no Hytale, cobrindo duracao, tons visuais, modificadores de atributos, dano ao longo do tempo e comportamento de sobreposicao.
---

## Visao Geral

Efeitos de entidade sao modificadores temporarios ou permanentes aplicados a entidades em tempo de execucao. Eles alimentam uma ampla gama de sistemas: tons visuais e sobreposicoes de tela ao receber dano, buffs de comida que aumentam a vida maxima, dano ao longo do tempo por queimaduras e veneno, efeitos de controle de grupo como enraizamento e atordoamento, e trilhas de particulas cosmeticas em habilidades de armas. Cada arquivo de efeito define sua duracao, regras de sobreposicao, modificacoes de atributos e feedback visual/sonoro.

## Localizacao dos Arquivos

```
Assets/Server/Entity/Effects/
```

Subdiretorios agrupam efeitos por categoria:

```
Assets/Server/Entity/Effects/
  BlockPlacement/     (feedback de sucesso/falha ao colocar blocos)
  Damage/             (efeitos de flash ao ser atingido)
  Deployables/        (auras de cura/lentidao de totens)
  Drop/               (efeitos de brilho de raridade de itens)
  Food/
    Boost/            (aumentos de atributos maximos por comida)
    Buff/             (curas instantaneas e buffs temporarios)
  GameMode/           (visual do modo criativo)
  Immunity/           (invulnerabilidade de esquiva, imunidade a fogo/ambiente)
  Mana/               (efeitos de regeneracao e dreno de mana)
  Movement/           (efeitos direcionais de esquiva)
  Npc/                (morte, cura, retorno ao lar de NPCs)
  Portals/            (visual de teleporte)
  Projectiles/        (sub-efeitos de flecha, bomba, escombros)
  Stamina/            (stamina quebrada, erro, atraso de regeneracao)
  Status/             (queimadura, congelamento, veneno, enraizamento, lentidao, atordoamento)
  Weapons/            (efeitos de assinatura e habilidade de armas)
```

## Schema

### Campos de nivel superior

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Duration` | `number` | Sim | — | Duracao do efeito em segundos. `0` ou `0.0` significa que o efeito dispara uma vez instantaneamente. |
| `Infinite` | `boolean` | Nao | `false` | Se `true`, o efeito persiste indefinidamente ate ser removido explicitamente. Sobrescreve `Duration`. |
| `OverlapBehavior` | `"Overwrite" \| "Extend"` | Nao | — | Como lidar com reaplicacao enquanto ja esta ativo. `Overwrite` substitui o temporizador; `Extend` adiciona a duracao restante. |
| `RemovalBehavior` | `string` | Nao | — | Como o efeito e removido. Valor conhecido: `"Duration"` (removido quando o temporizador expira). |
| `Debuff` | `boolean` | Nao | `false` | Se `true`, o efeito e classificado como debuff e pode ser limpo por interacoes do tipo antidoto. |
| `Invulnerable` | `boolean` | Nao | `false` | Se `true`, a entidade nao pode receber dano enquanto o efeito esta ativo. |
| `StatusEffectIcon` | `string` | Nao | — | Caminho para o icone de UI exibido na barra de efeitos de status. |
| `DeathMessageKey` | `string` | Nao | — | Chave de localizacao para a mensagem de morte quando este efeito mata uma entidade. |
| `ApplicationEffects` | `ApplicationEffects` | Nao | — | Modificacoes visuais, sonoras e de movimento aplicadas enquanto o efeito esta ativo. |
| `StatModifiers` | `object` | Nao | — | Mapa de ID de atributo para valor fixo adicionado por tick (ex: `{"Health": 2}`). |
| `ValueType` | `string` | Nao | — | Como os valores de `StatModifiers` sao interpretados. Valor conhecido: `"Percent"`. |
| `RawStatModifiers` | `object` | Nao | — | Mapa de ID de atributo para um array de objetos modificadores brutos para manipulacao avancada de atributos. |
| `DamageCalculator` | `DamageCalculator` | Nao | — | Dano periodico aplicado enquanto o efeito esta ativo. |
| `DamageCalculatorCooldown` | `number` | Nao | — | Segundos entre cada tick de dano do `DamageCalculator`. |
| `DamageEffects` | `object` | Nao | — | Eventos sonoros disparados em cada tick de dano. |
| `ModelOverride` | `ModelOverride` | Nao | — | Substitui o modelo visual da entidade pela duracao do efeito (ex: vinhas de enraizamento). |

### ApplicationEffects

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `EntityTopTint` | `string` | Nao | — | Cor hexadecimal aplicada a porcao superior do modelo da entidade. |
| `EntityBottomTint` | `string` | Nao | — | Cor hexadecimal aplicada a porcao inferior do modelo da entidade. |
| `ScreenEffect` | `string` | Nao | — | Caminho para uma textura de sobreposicao de tela (ex: `"ScreenEffects/Fire.png"`). |
| `HorizontalSpeedMultiplier` | `number` | Nao | — | Multiplicador aplicado a velocidade de movimento horizontal. `0.5` = 50% de velocidade. |
| `KnockbackMultiplier` | `number` | Nao | — | Multiplicador para repulsao recebida. `0` = imune a repulsao. |
| `ModelVFXId` | `string` | Nao | — | ID de um VFX em nivel de modelo para anexar a entidade. |
| `Particles` | `ParticleRef[]` | Nao | — | Lista de sistemas de particulas para gerar na entidade. |
| `MovementEffects` | `object` | Nao | — | Substituicoes de movimento. Contem `DisableAll: true` para imobilizar totalmente a entidade. |
| `WorldSoundEventId` | `string` | Nao | — | Evento sonoro audivel para todos os jogadores proximos. |
| `LocalSoundEventId` | `string` | Nao | — | Evento sonoro audivel apenas para o jogador afetado. |

### ParticleRef

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `SystemId` | `string` | Sim | — | ID do sistema de particulas a ser gerado. |
| `TargetEntityPart` | `string` | Nao | — | Parte da entidade a qual anexar a particula (ex: `"Entity"`). |
| `TargetNodeName` | `string` | Nao | — | Nome do osso ou no para anexacao (ex: `"Hip"`). |
| `PositionOffset` | `Vector3` | Nao | — | Deslocamento local a partir do ponto de anexacao. |
| `Color` | `string` | Nao | — | Substituicao de cor hexadecimal para o sistema de particulas. |

### RawStatModifier

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Amount` | `number` | Sim | — | Valor do modificador. A interpretacao depende do `CalculationType`. |
| `CalculationType` | `"Additive" \| "Multiplicative"` | Sim | — | `Additive` adiciona um valor fixo ao alvo; `Multiplicative` escala o alvo pelo valor. |
| `Target` | `string` | Sim | — | Qual aspecto do atributo modificar. Valor conhecido: `"Max"` (modifica o maximo do atributo). |

### DamageCalculator

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `BaseDamage` | `object` | Sim | — | Mapa de ID de tipo de dano para valor de dano (ex: `{"Fire": 5}`). |

### ModelOverride

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Model` | `string` | Sim | — | Caminho para o arquivo `.blockymodel` de substituicao. |
| `Texture` | `string` | Sim | — | Caminho para a textura de substituicao. |
| `AnimationSets` | `object` | Nao | — | Mapa de nome de estado de animacao para definicoes de animacao (ex: `Spawn`, `Despawn`). |

## Exemplos

**Efeito de status de queimadura** (`Assets/Server/Entity/Effects/Status/Burn.json`):

```json
{
  "ApplicationEffects": {
    "EntityBottomTint": "#100600",
    "EntityTopTint": "#cf2302",
    "ScreenEffect": "ScreenEffects/Fire.png",
    "WorldSoundEventId": "SFX_Effect_Burn_World",
    "LocalSoundEventId": "SFX_Effect_Burn_Local",
    "Particles": [{ "SystemId": "Effect_Fire" }],
    "ModelVFXId": "Burn"
  },
  "DamageCalculatorCooldown": 1,
  "DamageCalculator": {
    "BaseDamage": { "Fire": 5 }
  },
  "DamageEffects": {
    "WorldSoundEventId": "SFX_Effect_Burn_World",
    "PlayerSoundEventId": "SFX_Effect_Burn_Local"
  },
  "OverlapBehavior": "Overwrite",
  "Debuff": true,
  "StatusEffectIcon": "UI/StatusEffects/Burn.png",
  "Duration": 3,
  "DeathMessageKey": "server.general.deathCause.burn"
}
```

**Buff de comida com aumento de vida maxima** (`Assets/Server/Entity/Effects/Food/Boost/Food_Health_Boost_Large.json`):

```json
{
  "RawStatModifiers": {
    "Health": [
      {
        "Amount": 30,
        "CalculationType": "Additive",
        "Target": "Max"
      }
    ]
  },
  "Duration": 480,
  "OverlapBehavior": "Overwrite",
  "StatusEffectIcon": "UI/StatusEffects/AddHealth/Large.png"
}
```

**Invulnerabilidade de investida com adaga** (`Assets/Server/Entity/Effects/Weapons/Dagger_Dash.json`):

```json
{
  "Duration": 0.25,
  "ApplicationEffects": {
    "Particles": [
      {
        "SystemId": "Daggers_Dash_Straight",
        "TargetEntityPart": "Entity",
        "TargetNodeName": "Hip",
        "PositionOffset": { "Y": 1.0 },
        "Color": "#d7e5ec"
      }
    ],
    "ModelVFXId": "Dagger_Dash"
  },
  "OverlapBehavior": "Extend",
  "Invulnerable": true
}
```

## Paginas Relacionadas

- [Atributos de Entidade](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/entity-stats) — atributos modificados por efeitos
- [Tipos de Dano](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — IDs de tipo de dano usados no `DamageCalculator`
- [Configuracoes de Projeteis](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — projeteis que aplicam efeitos ao acertar
