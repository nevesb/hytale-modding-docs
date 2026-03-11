---
title: Criar uma Arma de Projétil
description: Tutorial passo a passo para criar uma arma de projétil com definições de projéteis, configurações de projéteis e cadeias de interação.
---

## Objetivo

Criar um **Cajado de Gelo** personalizado que dispara projéteis de raio de gelo. Você definirá a entidade do projétil, criará uma configuração de projétil que controla a física de lançamento e interações de impacto, e conectará tudo através da cadeia de interação da arma.

## O Que Você Vai Aprender

- Como definições de projéteis controlam aparência, física e dano
- Como configurações de projéteis conectam armas a projéteis com configurações de lançamento
- Como a cadeia de interação dispara projéteis no uso da arma
- Como interações de acerto e erro lidam com efeitos de impacto

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configurar Seu Ambiente de Desenvolvimento](/hytale-modding-docs/pt-br/tutorials/beginner/setup-dev-environment))
- Familiaridade com definições de itens (veja [Criar um Item Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-item))

---

## Visão Geral do Sistema de Projéteis

O sistema de projéteis do Hytale tem três camadas:

1. **Definição de Projétil** (`Assets/Server/Projectiles/`) -- define a entidade do projétil em si: aparência, física, dano e efeitos
2. **Configuração de Projétil** (`Assets/Server/ProjectileConfigs/`) -- conecta uma arma a um projétil com força de lançamento, sons e cadeias de interação para acerto/erro
3. **Item de Arma** -- referencia a configuração de projétil através de sua cadeia de interação

```
Item de Arma
  └─ referencia → Configuração de Projétil
                     └─ referencia → Definição de Projétil
```

---

## Passo 1: Criar a Definição do Projétil

Definições de projéteis descrevem o projétil físico que viaja pelo mundo. Os projéteis vanilla `Ice_Bolt.json` e `Arrow_FullCharge.json` são boas referências.

Crie:

```
YourMod/Assets/Server/Projectiles/Frost_Bolt.json
```

```json
{
  "Appearance": "Ice_Bolt",
  "Radius": 0.2,
  "Height": 0.2,
  "SticksVertically": true,
  "MuzzleVelocity": 45,
  "TerminalVelocity": 50,
  "Gravity": 5,
  "Bounciness": 0,
  "ImpactSlowdown": 0,
  "TimeToLive": 15,
  "Damage": 18,
  "DeadTimeMiss": 0,
  "DeathEffectsOnHit": true,
  "HorizontalCenterShot": 0.15,
  "VerticalCenterShot": 0.1,
  "DepthShot": 1.5,
  "PitchAdjustShot": true,
  "HitParticles": {
    "SystemId": "Impact_Ice"
  },
  "DeathParticles": {
    "SystemId": "Impact_Ice"
  },
  "HitSoundEventId": "SFX_Ice_Break",
  "MissSoundEventId": "SFX_Ice_Break",
  "DeathSoundEventId": "SFX_Ice_Break"
}
```

### Campos de projétil explicados

| Campo | Finalidade |
|-------|-----------|
| `Appearance` | O modelo visual para o projétil. Deve corresponder a um nome de aparência de projétil conhecido |
| `Radius` / `Height` | Dimensões da hitbox de colisão do projétil |
| `MuzzleVelocity` | Velocidade inicial de lançamento (unidades por segundo) |
| `TerminalVelocity` | Velocidade máxima que o projétil pode atingir |
| `Gravity` | Aceleração para baixo. Valores menores = trajetória mais reta. Flechas usam 10, raios de gelo usam 3-5 |
| `Bounciness` | Quanto o projétil quica no impacto. `0` = sem quique |
| `ImpactSlowdown` | Redução de velocidade no impacto. `0` = projétil para |
| `TimeToLive` | Segundos antes do projétil desaparecer se não acertar nada |
| `Damage` | Dano base causado no acerto |
| `SticksVertically` | Se `true`, o projétil se crava em superfícies quando erra |
| `DeadTimeMiss` | Segundos que o projétil permanece depois de errar. `0` = desaparece imediatamente |
| `DeathEffectsOnHit` | Se `true`, partículas de morte tocam no acerto assim como na expiração natural |
| `HorizontalCenterShot` / `VerticalCenterShot` | Dispersão de precisão. Valores menores = mais preciso. `0` = perfeitamente centralizado |
| `DepthShot` | Deslocamento frontal do personagem quando o projétil é gerado |
| `PitchAdjustShot` | Se `true`, o ângulo inicial do projétil corresponde à inclinação da mira do jogador |
| `HitParticles` / `DeathParticles` | IDs de sistema de efeito de partículas tocados no acerto ou morte |
| `HitSoundEventId` / `MissSoundEventId` | Eventos de som para impacto e erro |

---

## Passo 2: Criar a Configuração do Projétil

A configuração de projétil conecta uma arma a um projétil. Ela especifica força de lançamento, sobrescritas de física, sons e a cadeia de interação que executa no acerto ou erro. Configurações ficam em `Assets/Server/ProjectileConfigs/`.

Crie:

```
YourMod/Assets/Server/ProjectileConfigs/Weapons/Staff/Projectile_Config_Frost_Staff.json
```

```json
{
  "Model": "Ice_Bolt",
  "LaunchForce": 20,
  "Physics": {
    "Type": "Standard",
    "Gravity": 5,
    "TerminalVelocityAir": 50,
    "TerminalVelocityWater": 15,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": true
  },
  "LaunchLocalSoundEventId": "SFX_Staff_Shoot_Local",
  "LaunchWorldSoundEventId": "SFX_Staff_Shoot",
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        {
          "Type": "Replace",
          "Var": "Primary_Shoot_Damage",
          "DefaultValue": {
            "Interactions": [
              "Weapon_Staff_Frost_Damage"
            ]
          }
        },
        {
          "Type": "Replace",
          "Var": "Primary_Shoot_Impact",
          "DefaultValue": {
            "Interactions": [
              "Common_Projectile_Impact_Effects"
            ]
          }
        },
        "Common_Projectile_Despawn"
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        {
          "Type": "Replace",
          "Var": "Primary_Shoot_Miss",
          "DefaultValue": {
            "Interactions": [
              "Common_Projectile_Miss"
            ]
          }
        },
        "Common_Projectile_Despawn"
      ]
    }
  }
}
```

### Campos de configuração de projétil

| Campo | Finalidade |
|-------|-----------|
| `Model` | O modelo de aparência do projétil a usar |
| `LaunchForce` | Força aplicada ao disparar. Maior = velocidade inicial mais rápida |
| `Physics.Type` | Tipo de simulação física. `"Standard"` é o padrão |
| `Physics.Gravity` | Sobrescrita de gravidade para a configuração (sobrescreve o valor da definição do projétil) |
| `Physics.TerminalVelocityAir` / `TerminalVelocityWater` | Velocidade máxima no ar e na água |
| `Physics.RotationMode` | Como o projétil rotaciona em voo. `"VelocityDamped"` faz ele virar na direção do deslocamento |
| `Interactions.ProjectileHit` | Cadeia de interação executada quando o projétil acerta uma entidade |
| `Interactions.ProjectileMiss` | Cadeia de interação executada quando o projétil acerta terreno ou expira |

### Estrutura da cadeia de interação

O objeto `Interactions` usa um padrão de variável-substituição. Cada entrada com `"Type": "Replace"` define uma variável nomeada (`Var`) com um `DefaultValue` contendo referências de interação. Isso permite que templates sobrescrevam partes específicas da cadeia. As entradas de string (como `"Common_Projectile_Despawn"`) referenciam arquivos de interação compartilhados.

---

## Passo 3: Criar o Item de Arma

O item de arma referencia a configuração de projétil através de sua configuração de interação. Crie a definição do item do cajado:

```
YourMod/Assets/Server/Item/Items/Weapon/Weapon_Staff_Frost.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Weapon_Staff_Frost.name",
    "Description": "server.items.Weapon_Staff_Frost.description"
  },
  "Icon": "Icons/MyMod/Weapon_Staff_Frost.png",
  "Quality": "Rare",
  "MaxStack": 1,
  "ItemLevel": 5,
  "Interactions": {
    "Primary": "Staff_Frost_Primary_Shoot",
    "Secondary": "Staff_Frost_Secondary_Block"
  },
  "ProjectileConfig": "Projectile_Config_Frost_Staff",
  "Recipe": {
    "TimeSeconds": 8,
    "Input": [
      {
        "ItemId": "Ingredient_Bar_Iron",
        "Quantity": 5
      },
      {
        "ItemId": "Ingredient_Ice_Essence",
        "Quantity": 10
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 3
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Weapon_Bench",
        "Categories": [
          "Weapon_Bow"
        ]
      }
    ]
  },
  "PlayerAnimationsId": "Staff",
  "Tags": {
    "Type": [
      "Weapon"
    ],
    "Family": [
      "Staff"
    ]
  },
  "ItemSoundSetId": "ISS_Weapons_Staff"
}
```

### Campos principais da arma

| Campo | Finalidade |
|-------|-----------|
| `Interactions.Primary` | O arquivo de interação acionado no ataque primário (clique esquerdo). Esta cadeia de interação finalmente dispara o projétil |
| `Interactions.Secondary` | O arquivo de interação acionado na ação secundária (clique direito) |
| `ProjectileConfig` | Referencia o arquivo de configuração de projétil pelo nome (sem `.json`). Isto é o que conecta a arma ao seu projétil |

---

## Passo 4: Adicionar Chaves de Tradução

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Weapon_Staff_Frost.name=Frost Staff
server.items.Weapon_Staff_Frost.description=A staff that fires bolts of freezing ice.
```

---

## Passo 5: Testar No Jogo

1. Coloque sua pasta de mod no diretório de mods do servidor.
2. Inicie o servidor e observe erros sobre configurações de projétil desconhecidas ou arquivos de interação ausentes.
3. Use o gerador de itens do desenvolvedor para obter `Weapon_Staff_Frost`.
4. Equipe o cajado e use ataque primário (clique esquerdo) para disparar o projétil.
5. Verifique que o projétil viaja com o arco correto (gravidade), velocidade e aparência.
6. Acerte um NPC e confirme que o dano é aplicado e as partículas de impacto tocam.
7. Dispare no terreno e confirme que o som de erro e partículas tocam.
8. Verifique que o projétil desaparece após `TimeToLive` segundos se não acertar nada.

**Erros comuns e correções:**

| Erro | Causa | Correção |
|------|-------|----------|
| `Unknown projectile config` | Arquivo de configuração não encontrado | Verifique o caminho do arquivo sob `ProjectileConfigs/` e se o nome do arquivo corresponde ao valor de `ProjectileConfig` |
| Projétil voa direto para cima | `PitchAdjustShot` é false | Defina `"PitchAdjustShot": true` |
| Projétil cai muito rápido | `Gravity` muito alta | Reduza a gravidade. Flechas usam 10, projéteis mágicos usam 3-5 |
| Sem visual no projétil | `Appearance` errado | Verifique `Assets/Server/Models/Projectiles/` para nomes de aparência válidos |
| Sem dano no acerto | `Damage` é 0 ou interações ausentes | Defina `Damage` > 0 e verifique a cadeia de interação `ProjectileHit` |

---

## Próximos Passos

- [Criar um Item Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-item) -- entenda a estrutura completa de definição de item
- [Criar uma Bancada de Trabalho](/hytale-modding-docs/pt-br/tutorials/intermediate/create-a-crafting-bench) -- construa a bancada onde jogadores fabricam sua arma
- [Tabelas de Loot Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-loot-tables) -- faça sua arma dropar de inimigos
