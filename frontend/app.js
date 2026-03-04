const form = document.getElementById("form");
const quizError = document.getElementById("quizError");
const quizResult = document.getElementById("quizResult");
let checkBoxElement = document.getElementsByName("profil");
let lastSubmissionId = null;

async function onSubmit(event) {
  event.preventDefault();
  quizError.textContent = "";
  quizResult.textContent = "";
  quizError.style.display = "none";

  let checked = [];
  let answersText = [];
  checkBoxElement.forEach((element) => {
    if (element.checked == true) {
      checked.push(element.value);
      const label = element.closest("label");
      const p = label.querySelector("p");
      answersText.push(p.textContent.trim());
    }
  });

  const payload = { selectedInForm: checked, answersText };
  try {
    // Appel API
    const response = await fetch("/quiz/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      const message = data?.detail?.message ?? "Une erreur est survenue.";
      quizError.textContent = message;
      quizError.style.display = "block";
      return;
    }

    const percentages = data.percentages;
    const top1 = data.top1;
    lastSubmissionId = data.submission_id;

    let linePercentages = `<div class="results-stats">`;

    for (const [profil, value] of Object.entries(percentages)) {
      linePercentages += `
            <div class="stat-item">
                <div class="stat-label">
                    <span>${profil.charAt(0).toUpperCase() + profil.slice(1)}</span>
                    <span> ${value}%</span>
                </div>
                <div class="progress-container">
                    <div class="progress-fill ${profil}" style="width: ${value}%"></div>
                </div>
            </div>`;
    }
    linePercentages += `</div>`;

    // Déterminer le profil dominant
    let dominantsTexts = {
      sanguin: `C'est le bon vivant, le "soleil" de la pièce. Toujours en mouvement, il parle avec les mains, rit fort et oublie ses clés trois fois par jour. Son humeur est comme le printemps : radieuse, mais sujette aux averses soudaines.
<br><br><strong>Le conseil :</strong> Apprenez à finir ce que vous commencez. On sait que votre nouvelle passion pour le ukulélé est intense, mais essayez de dépasser la première leçon.
<br><strong>À éviter :</strong> Les régimes draconiens et la solitude prolongée. Vous avez besoin de monde pour briller, sinon vous vous fanez comme une plante sans eau.`,
      bilieux: `Voici le leader né, celui qui a déjà organisé le planning des vacances avant même que vous ayez choisi la destination. Il est énergique, déterminé et possède un regard qui pourrait faire bouillir une bouilloire à distance.
<br><br><strong>Le conseil :</strong> Travaillez votre patience. Tout le monde ne roule pas à 200 km/h comme vous, et c'est (parait-il) très bien ainsi.
<br><strong>À éviter :</strong> Les tête-à-tête avec d'autres Bilieux sans arbitre, et le café en excès. Vous êtes déjà naturellement sous tension, inutile de rajouter de l'huile sur le feu.`,
      lymphatique: `La force tranquille. Rien ne semble l'atteindre. Il est calme, fiable, un peu lent (diront les mauvaises langues), mais c'est le meilleur ami que l'on puisse avoir pour garder la tête froide en pleine tempête.
<br><br><strong>Le conseil :</strong> Un peu d'exercice physique ne vous fera pas de mal. On ne parle pas d'un marathon, mais bouger un peu aidera votre "humeur" à ne pas stagner.
<br><strong>À éviter :</strong> La procrastination poussée au rang d'art majeur. "On verra demain" est une phrase dangereuse pour vous, car demain a tendance à devenir "le mois prochain".`,
      nerveux: `C'est l'intellectuel, le perfectionniste, l'artiste tourmenté. Il analyse tout, prévoit les catastrophes avant qu'elles n'arrivent et possède une vie intérieure plus dense qu'un dictionnaire.
<br><br><strong>Le conseil :</strong> Sortez de votre tête de temps en temps ! Le monde réel est parfois moins effrayant que les scénarios que vous échafaudez pendant vos insomnies.
<br><strong>À éviter :</strong> Les actualités anxiogènes avant de dormir et l'autocritique permanente. Soyez aussi indulgent avec vous-même qu'avec vos livres préférés.`,
    };

    let resultHTML = "";

    if (top1.length === 1) {
      resultHTML = `
        <h2 class="result-main-title">Votre Profil Dominant : ${top1[0].toUpperCase()}</h2>
        <div class="card result-card">
          <p class="result-description">${dominantsTexts[top1[0]]}</p>
        </div>`;
    } else if (top1.length > 1) {
      resultHTML = `
            <h2 class="result-main-title">Profils dominants ex æquo</h2>
            <div class="card result-card multi-intro">
                <p>Félicitations, vous ne rentrez pas dans une seule case ! Si vos résultats affichent une égalité, c'est que votre nature refuse de se laisser simplifier. Dans la tradition d'Hippocrate, on appelle cela un tempérament composé.
Loin d'être une indécision de la nature, cette dualité (ou pluralité) signifie que vous possédez plusieurs cordes à votre arc pour interagir avec le monde :
Une adaptabilité accrue : Vous pouvez passer de l'action à la réflexion, ou du calme à l'enthousiasme selon le contexte.
Un équilibre protecteur : Souvent, un tempérament vient tempérer les excès de l'autre.
Une richesse intérieure : Vous n'êtes pas un seul paysage, mais tout un écosystème. Votre défi consiste à harmoniser ces énergies parfois contradictoires pour ne pas vous sentir "tiraillé".
En naturopathie, cette égalité est vue comme une invitation à cultiver votre propre homéostasie : puisez dans la force de chacun de vos profils dominants pour construire une hygiène de vie qui vous ressemble, sans jamais vous enfermer dans une étiquette unique.
Voici les précisions sur vos différents profils : </p>
            </div>`;

      top1.forEach((profil) => {
        resultHTML += `
                <div class="profile-detail-block">
                    <h3 class="subtitle">${profil.toUpperCase()}</h3>
                    <p>${dominantsTexts[profil]}</p>
                </div>`;
      });
    }

    const emailSection = `
  <div class="email-capture-container">
    <div class="email-content">
      <h3 class="email-title">Recevoir votre rapport complet</h3>
      <p class="email-subtitle">Obtenez vos conseils personnalisés et votre guide d'hygiène de vie par email.</p>
      
      <form id="emailForm" class="email-form">
        <input 
          type="email" 
          id="userEmail" 
          placeholder="votre@email.com" 
          required 
          class="email-input"
        >
        <button type="submit" id="sendReportBtn" class="email-submit-btn">
          <span>Envoyer le rapport</span>
        </button><br>
        <input type="checkbox" id="isConsent" name="isConsent"/>
        <label for="isConsent" class="consent-label">J'accepte de recevoir mon rapport complet par email.</label>
      
      <div id="emailMessage" class="email-status-message"></div></form>
    </div>
  </div>
`;

    // Affichage final
    quizResult.innerHTML = linePercentages + resultHTML + emailSection;
    quizResult.style.display = "block";
    quizResult.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    console.error(err);
    quizError.innerHTML =
      "<strong>Oups !</strong> Impossible de contacter le serveur. Réessaie.";
    quizError.style.display = "block";
  }

  // Récupère le nouveau formulaire d'email
  const emailForm = document.getElementById("emailForm");
  if (emailForm) {
    emailForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const email = document.getElementById("userEmail").value;
      const msg = document.getElementById("emailMessage");
      const isConsent = document.getElementById("isConsent").checked;

      if (!isConsent) {
        msg.style.display = "block";
        msg.style.color = "#c0392b";
        msg.textContent = "Veuillez accepter les conditions d'utilisation.";
        return;
      }
      if (!lastSubmissionId) {
        msg.style.display = "block";
        msg.style.color = "#c0392b";
        msg.textContent =
          "Erreur: submission_id introuvable. Revalide le quiz.";
        return;
      }

      const payload = {
        submission_id: lastSubmissionId,
        email: email,
        consent: isConsent,
      };
      try {
        // Appel API
        const response = await fetch("/report/send", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
          const message = data?.detail?.message ?? "Erreur serveur.";
          throw new Error(message);
        }
        msg.style.display = "block";
        msg.style.color = "#4d785c";
        msg.textContent = "Merci ! Votre rapport est en route vers " + email;
      } catch (err) {
        console.error("Erreur lors de l'envoi du rapport :", err);
        msg.style.display = "block";
        msg.style.color = "#c0392b";
        msg.textContent = "Oups ! Impossible d'envoyer le rapport. Réessaie.";
      }
    });
  }
}
form.addEventListener("submit", onSubmit);
