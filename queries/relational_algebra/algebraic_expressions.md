# Module 1: Relational Query Languages & Relational Algebra Expressions

This document demonstrates the theoretical foundations of relational query languages using formal Relational Algebra operations on the relational reference schema for the **GRAMMY Awards Information & Analytics System**.

All expressions utilize standard mathematical relational algebra notation:
- **Selection**: $\sigma_{\text{condition}}(R)$
- **Projection**: $\pi_{\text{attribute\_list}}(R)$
- **Cartesian Product**: $R \times S$
- **Natural Join**: $R \bowtie S$
- **Theta Join / Equijoin**: $R \bowtie_{\theta} S$
- **Union**: $R \cup S$
- **Intersection**: $R \cap S$
- **Set Difference**: $R - S$
- **Renaming**: $\rho_{S}(R)$ or $\rho_{A \to B}(R)$
- **Division**: $R \div S$

---

## Query 1: Selection ($\sigma$) & Projection ($\pi$)
**Domain Query**: *Retrieve the ceremony edition, broadcast year, and host city for all GRAMMY ceremonies held in Los Angeles where more than 80 total awards were presented.*

### Relational Algebra Expression:
$$\pi_{\text{edition\_number, broadcast\_year, host\_city}}\left( \sigma_{\text{host\_city} = \text{'Los Angeles'} \;\land\; \text{total\_awards\_presented} > 80}(\text{ceremonies}) \right)$$

### Query Tree:
```text
          π(edition_number, broadcast_year, host_city)
                           |
          σ(host_city = 'Los Angeles' ∧ total_awards_presented > 80)
                           |
                      ceremonies
```

---

## Query 2: Equijoin ($\bowtie_{\theta}$) & Selection
**Domain Query**: *Find the stage name of all artists who received an Album of the Year nomination in the 65th Annual GRAMMY Awards, along with the title of their nominated work.*

### Relational Algebra Expression:
$$\pi_{\text{artists.stage\_name, nominated\_works.work\_title}}\left( \sigma_{\text{ceremony\_id} = \text{'CEREMONY\_065'} \;\land\; \text{category\_id} = \text{'CAT\_AOTY'}}(\text{nomination\_entries}) \bowtie_{\text{nomination\_entries.work\_id} = \text{nominated\_works.work\_id}} \text{nominated\_works} \bowtie_{\text{nomination\_entries.primary\_artist\_id} = \text{creators.creator\_id}} \text{creators} \right)$$

---

## Query 3: Set Union ($\cup$)
**Domain Query**: *List all creators who have served as a ceremony host OR have received a Special Merit Lifetime Achievement Award.*

### Relational Algebra Expression:
$$\pi_{\text{creator\_id}}(\text{ceremony\_hosts}) \;\cup\; \pi_{\text{recipient\_creator\_id} \to \text{creator\_id}}(\text{lifetime\_achievement\_honors})$$

*Condition*: Both relations are union-compatible as they project a single compatible attribute domain ($\text{creator\_id}$).

---

## Query 4: Set Difference ($-$)
**Domain Query**: *Find all artists who have received at least one GRAMMY nomination but have never won a GRAMMY award.*

### Relational Algebra Expression:
$$\text{AllNominatedArtists} \leftarrow \pi_{\text{primary\_artist\_id}}(\text{nomination\_entries})$$
$$\text{WinningArtists} \leftarrow \pi_{\text{primary\_artist\_id}}(\text{winner_records})$$
$$\text{Result} \leftarrow \text{AllNominatedArtists} - \text{WinningArtists}$$

---

## Query 5: Natural Join ($\bowtie$) & Renaming ($\rho$)
**Domain Query**: *Find all active categories and their corresponding genre field name where the category allows a maximum of more than 5 nominees.*

### Relational Algebra Expression:
$$\rho_{F}(\text{award\_fields})$$
$$\rho_{C}(\text{award\_categories})$$
$$\pi_{C.\text{official\_category\_name}, F.\text{field\_name}}\left( \sigma_{C.\text{maximum\_nominees\_allowed} > 5 \;\land\; C.\text{current\_status} = \text{'Active'}}(C \bowtie_{C.\text{field\_id} = F.\text{field\_id}} F) \right)$$

---

## Query 6: Cartesian Product ($\times$) & Theta Selection
**Domain Query**: *Evaluate the theoretical pairing matrix between all venues located in 'Los Angeles' and all ceremonies broadcast on the 'CBS' network.*

### Relational Algebra Expression:
$$\text{LAVenues} \leftarrow \sigma_{\text{city} = \text{'Los Angeles'}}(\pi_{\text{venue\_id, venue\_name}}(\text{venues}))$$
$$\text{CBSCeremonies} \leftarrow \sigma_{\text{primary\_network} = \text{'CBS'}}(\pi_{\text{ceremony\_id, edition\_number}}(\text{ceremonies}))$$
$$\text{Result} \leftarrow \text{LAVenues} \times \text{CBSCeremonies}$$

---

## Query 7: Three-Way Join Composition
**Domain Query**: *Retrieve the venue name, ceremony edition, and average US viewership in millions for all ceremonies that generated over 20 million viewers.*

### Relational Algebra Expression:
$$\pi_{\text{venues.venue\_name, ceremonies.edition\_number, viewership\_ratings.us\_viewers\_millions}}\left( \sigma_{\text{us\_viewers\_millions} > 20.0}\left( \text{viewership\_ratings} \bowtie_{\text{viewership\_ratings.ceremony\_id} = \text{ceremonies.ceremony\_id}} \text{ceremonies} \bowtie_{\text{ceremonies.venue\_id} = \text{venues.venue\_id}} \text{venues} \right) \right)$$

---

## Query 8: Division Operator ($\div$)
**Domain Query**: *Find the creator_id of all artists who have won an award in EVERY category belonging to the 'Pop' field.*

### Problem Formulation:
Let $R$ be the relation containing all artist IDs and the category IDs they have won in:
$$R \leftarrow \pi_{\text{primary\_artist\_id}, \text{category\_id}}(\text{winner\_records})$$
Let $S$ be the relation of all category IDs currently in the 'Pop' field (`FLD_POP`):
$$S \leftarrow \pi_{\text{category\_id}}\left( \sigma_{\text{field\_id} = \text{'FLD\_POP'}}(\text{award\_categories}) \right)$$

### Relational Algebra Expression:
$$\text{Result} \leftarrow R \div S$$

### Formal Definition of Division:
$$R \div S = \pi_{\text{primary\_artist\_id}}(R) - \pi_{\text{primary\_artist\_id}}\left( (\pi_{\text{primary\_artist\_id}}(R) \times S) - R \right)$$

---

## Query 9: Aggregation & Grouping ($\gamma$)
**Domain Query**: *For each record label, count the total number of distinct nominated works in the system.*

### Relational Algebra Expression:
$$\gamma_{\text{primary\_label\_id};\; \text{COUNT}(\text{work\_id}) \to \text{total\_nominated\_works}}(\text{nominated\_works})$$

---

## Query 10: Multi-Condition Complex Filter with Projection
**Domain Query**: *Find the statuette serial numbers and recipient creator IDs for all physical trophies manufactured from 'Grammium' alloy with a 24k gold plating thickness of at least 5.0 microns, for ceremonies occurring after 2010.*

### Relational Algebra Expression:
$$\text{ModernCeremonies} \leftarrow \sigma_{\text{broadcast\_year} > 2010}(\text{ceremonies})$$
$$\text{ValidTrophies} \leftarrow \sigma_{\text{grammium\_alloy\_specification} = \text{'Grammium-A'} \;\land\; \text{gold\_plating\_thickness\_microns} \ge 5.0}(\text{trophy\_tracking})$$
$$\pi_{\text{statuette\_serial\_number, recipient\_creator\_id}}\left( \text{ValidTrophies} \bowtie_{\text{ValidTrophies.winner\_record\_id} = \text{winner\_records.winner\_record\_id}} \text{winner\_records} \bowtie_{\text{winner\_records.ceremony\_id} = \text{ModernCeremonies.ceremony\_id}} \text{ModernCeremonies} \right)$$
