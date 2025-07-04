import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

def generate_individual_interviews():
    """Generate individual interview transcripts"""
    return [
        {
            'participant_id': 'INT_001',
            'data_type': 'individual_interview',
            'interview_type': 'Emotional Impact & Trust',
            'role': 'Marketing Manager',
            'age': 34,
            'focus_areas': 'emotional_responses, trust, deception_feelings, stress, organizational_relationship',
            'transcript_text': """
RESEARCHER: How did you feel immediately after realizing it was a phishing simulation?

PARTICIPANT: Honestly, I felt a complex mix of emotions. Initially, there was this wave of relief washing over me because I realized my personal data and our company's information wasn't actually compromised. But that relief was quickly followed by a deep sense of embarrassment and shame. I pride myself on being tech-savvy - I'm the person my family comes to for computer problems, you know? So falling for this felt like a personal failure.

RESEARCHER: Can you elaborate on that feeling of shame?

PARTICIPANT: It was profound. I kept thinking about how I always lecture my parents about being careful online, and here I was, clicking on a suspicious link without hesitation. The worst part was wondering who else knew I had fallen for it. Would this affect how my colleagues perceive my competence? Would management question my judgment in other areas?

RESEARCHER: Did you feel deceived by the organization conducting this experiment?

PARTICIPANT: That's complicated. My initial reaction was feeling betrayed - like the organization was spying on us, testing us without our knowledge. It felt invasive and manipulative. I kept thinking, 'How long have they been watching our email behavior?' But after the comprehensive debrief session, I began to understand the educational purpose. The security team explained how these simulations are industry best practices, and they showed us statistics about real phishing attacks affecting similar companies. That context helped me reframe the experience.

RESEARCHER: How has this experience changed your relationship with the organization?

PARTICIPANT: It's evolved. Initially, it damaged my trust - I felt like they were being deceptive. But over time, I've come to appreciate their proactive approach. They could have waited for a real attack to happen, which would have been much worse. Now I see it as the organization investing in our security education rather than just catching us in mistakes. However, I do think the communication could have been better. Maybe a general announcement about upcoming security assessments without specific details would have felt less deceptive.

RESEARCHER: How has your attitude toward email security changed?

PARTICIPANT: It's completely transformed. I'm much more paranoid now, and I mean that in a positive way. I hover over every link before clicking, I scrutinize sender addresses for subtle misspellings, and I pay attention to the tone and urgency of messages. Sometimes I feel anxious opening emails, especially those marked as urgent or coming from executives I don't regularly communicate with. The simulation taught me that being generally careful isn't enough - you need to be systematically vigilant.

RESEARCHER: Has this anxiety been manageable?

PARTICIPANT: It was overwhelming at first. I found myself second-guessing every email interaction, which was time-consuming and stressful. But the follow-up training sessions helped me develop more efficient verification strategies. Now I have a mental checklist that doesn't take much time but gives me confidence in my decisions.

RESEARCHER: Do you feel the intervention met your psychological needs?

PARTICIPANT: In some ways, yes, and in others, no. It definitely satisfied my need for competence because I learned concrete skills that I can apply daily. The training materials were comprehensive, and practicing with additional simulated emails helped build my confidence. It also met my need for autonomy - I now feel more in control of my digital security rather than just hoping for the best. However, it initially damaged my sense of competence and made me question my judgment. The key was the supportive follow-up that helped rebuild my confidence while maintaining the important lessons learned.

RESEARCHER: How do you view your role in organizational security now?

PARTICIPANT: I see myself as an active participant rather than a passive recipient of IT security measures. Before, I thought security was IT's job, and my role was just to follow basic rules. Now I understand that every email I receive is a potential security decision that could affect the entire organization. It's both empowering and somewhat burdensome, but ultimately I prefer feeling like I have agency in protecting our workplace.
            """,
            'word_count': 635,
            'data_collection_date': datetime.now() - timedelta(days=random.randint(1, 90))
        },
        {
            'participant_id': 'INT_002',
            'data_type': 'individual_interview', 
            'interview_type': 'Cognitive Change & Learning',
            'role': 'IT Support Specialist',
            'age': 29,
            'focus_areas': 'cognitive_changes, behavioral_adaptation, learning_outcomes, self_efficacy',
            'transcript_text': """
RESEARCHER: What was your immediate reaction when you discovered the phishing email was fake?

PARTICIPANT: Actually, I didn't fall for it initially. I reported it immediately to our security team, so when I found out it was a test, I felt validated and somewhat proud. Like, 'See? I know what I'm doing.' It boosted my confidence in my security knowledge and reinforced that my training and experience were paying off. But that confidence was tempered by concern for my colleagues who might have clicked.

RESEARCHER: How did you feel about colleagues who did fall for the simulation?

PARTICIPANT: I felt empathetic rather than superior. Working in IT support, I see how overwhelming technology can be for people whose expertise lies elsewhere. The simulation made me more aware of the human element in security. Technical solutions like firewalls and antivirus software are only part of the puzzle - human decision-making is often the most vulnerable point. It reinforced my belief that we need better user education, not just better technology.

RESEARCHER: How has your thinking about cybersecurity evolved?

PARTICIPANT: Before the simulation, I was very focused on technical aspects - patch management, system configurations, monitoring tools. But seeing the results opened my eyes to the psychological and social engineering components of attacks. I started reading about cognitive biases, social psychology, and how attackers exploit human psychology. It's fascinating and terrifying how sophisticated these attacks have become.

RESEARCHER: What specific cognitive strategies have you developed?

PARTICIPANT: I've developed a more systematic approach to email analysis. Instead of just trusting my gut instinct, I now have a mental framework. I ask myself: Do I know this sender? Was I expecting this communication? Does the request make sense in context? Is there artificial urgency or emotional manipulation? I also try to think like an attacker - what would I do to trick someone in my position or in the recipient's position?

RESEARCHER: How has your behavior at work changed?

PARTICIPANT: I've become more proactive in helping colleagues with security questions. I used to wait for people to come to me with problems, but now I regularly share tips during team meetings and help people analyze questionable emails. I've also started documenting common attack patterns I see, both in simulations and real attempts, to help train others.

RESEARCHER: Has this role expansion been welcomed by colleagues?

PARTICIPANT: Mostly yes. People appreciate having someone they can ask without feeling judged. The simulation helped normalize security concerns - it's no longer embarrassing to say you're unsure about an email. However, I've had to be careful not to come across as condescending or create anxiety where none existed before.

RESEARCHER: How do you assess your current preparedness level?

PARTICIPANT: I feel more prepared than before, but I'm also more aware of how unprepared we all are for truly sophisticated attacks. The simulation showed me that attackers are constantly evolving their techniques. I need to stay updated on new attack vectors, understand emerging social engineering tactics, and maintain my vigilance without becoming paralyzed by paranoia.

RESEARCHER: What learning outcomes surprised you most?

PARTICIPANT: The biggest surprise was realizing how much context matters in security decisions. The same email might be legitimate or suspicious depending on timing, recent events in the organization, or even the recipient's current stress level. This made me understand that security training can't just be about recognizing technical indicators - it has to include situational awareness and decision-making under uncertainty.

RESEARCHER: How sustainable are these new practices?

PARTICIPANT: The intense vigilance phase lasted about a month, then settled into more sustainable habits. The key was practicing the new behaviors until they became automatic. Now, the cognitive framework I developed runs in the background without requiring conscious effort most of the time. It only becomes deliberate when something triggers my suspicion.
            """,
            'word_count': 612,
            'data_collection_date': datetime.now() - timedelta(days=random.randint(1, 90))
        },
        {
            'participant_id': 'INT_003',
            'data_type': 'individual_interview',
            'interview_type': 'Behavioral Change & Stress Management',
            'role': 'Finance Director',
            'age': 45,
            'focus_areas': 'behavioral_adaptation, stress_management, decision_making, leadership_perspective',
            'transcript_text': """
RESEARCHER: How has your thinking about cybersecurity changed since the simulation?

PARTICIPANT: The simulation fundamentally shifted my perspective from viewing cybersecurity as IT's responsibility to understanding it as everyone's responsibility, especially those of us in leadership positions. Before, I thought my role was just to approve security budgets and ensure compliance. Now I realize that every financial email I open, every request I approve, is a potential security decision that could impact the entire organization.

RESEARCHER: Can you describe specific behavioral changes you've implemented?

PARTICIPANT: Absolutely. I used to click first and think later, especially with emails marked urgent or coming from executives. The pressure of financial deadlines often overrode caution. Now I have a systematic approach: I pause, take a deep breath, and analyze before acting. For financial requests, even those that seem legitimate, I've implemented a verification protocol. I call the requester using a known phone number, not one provided in the email. This extra step has already helped me catch two suspicious requests that weren't part of any simulation.

RESEARCHER: How do you manage the time pressure versus security dilemma?

PARTICIPANT: That's been the biggest challenge. Finance operates on tight deadlines, and adding verification steps can slow down legitimate transactions. I've had to educate my team and other departments about these new protocols. Initially, there was pushback about delays, but when I explained the potential cost of a successful attack - both financial and reputational - people became more understanding. We've actually found that most 'urgent' requests aren't truly urgent when examined closely.

RESEARCHER: What cognitive strategies do you employ now?

PARTICIPANT: I try to think like an attacker targeting someone in my position. What would I do to trick a finance director? I'd probably create urgency around a payment, impersonate a CEO or board member, or exploit my knowledge of our financial processes. This perspective shift has been eye-opening. I now look for social engineering tactics, not just technical indicators. I pay attention to unusual timing, emotional manipulation, and requests that bypass normal procedures.

RESEARCHER: How has this affected your stress levels?

PARTICIPANT: Initially, it increased my stress significantly. I became anxious about every email, worried about making mistakes that could compromise our financial systems. But over time, having systematic processes has actually reduced my stress. I'm more confident in my decisions because I know I've followed a thorough evaluation process. The anxiety has transformed into productive vigilance.

RESEARCHER: How do you handle the psychological pressure of being a target?

PARTICIPANT: It was unsettling to realize how attractive a target I am for attackers. As someone who approves large transactions and has access to sensitive financial information, I represent a high-value target. But this awareness has made me more strategic about my security practices. I've also become more conscious of what information I share publicly, including on social media and professional networks.

RESEARCHER: How confident are you in your current abilities?

PARTICIPANT: I'm more confident than before, but it's a realistic confidence based on process rather than intuition. I know my limitations and when to seek help from our security team. The simulation taught me that overconfidence is dangerous - attackers are sophisticated and constantly evolving their techniques.

RESEARCHER: What impact has this had on your leadership approach?

PARTICIPANT: I've become more proactive about security awareness in my department. We now include security considerations in our regular team meetings, and I encourage people to ask questions about suspicious emails without fear of judgment. I've also advocated for additional security training budget and worked with IT to develop finance-specific threat scenarios for practice.

RESEARCHER: Any concerns about creating a culture of fear?

PARTICIPANT: That's something I monitor carefully. The goal is to create appropriate caution, not paralyzing fear. I emphasize that security is a team effort and that asking questions shows good judgment, not incompetence. We celebrate successful threat identification rather than punishing mistakes, which has helped maintain a positive learning environment.
            """,
            'word_count': 648,
            'data_collection_date': datetime.now() - timedelta(days=random.randint(1, 90))
        }
    ]

def generate_focus_groups():
    """Generate focus group transcripts"""
    return [
        {
            'participant_id': 'FG_001',
            'data_type': 'focus_group',
            'interview_type': 'Organizational Trust & Culture Change',
            'role': '8 participants (mixed roles)',
            'age': 'Mixed ages 26-52',
            'focus_areas': 'organizational_trust, culture_change, peer_support, training_effectiveness, communication',
            'transcript_text': """
FACILITATOR: Let's begin by discussing how the phishing simulation affected your trust in the organization. I'd like to hear from everyone about their initial reactions.

PARTICIPANT_A (HR Manager, 38): Initially, I felt completely betrayed. Like the company was conducting surveillance on us without our knowledge or consent. My first thought was, 'What else are they monitoring that we don't know about?' It felt like a violation of the psychological contract between employer and employee. I understand the need for security, but the method felt deceptive and manipulative.

PARTICIPANT_B (Sales Representative, 29): I had the opposite reaction, actually. I felt like the organization cared enough about our security and the company's protection to invest in realistic, effective training. Too many companies just do generic security awareness presentations that nobody remembers. This showed they were serious about protecting us from real threats we face every day.

PARTICIPANT_C (Accountant, 44): My concern was more about judgment and performance evaluation. Would management think less of those who fell for the simulation? Would it affect our performance reviews or advancement opportunities? The fear of being labeled as a 'security risk' was very real, even though they said it was just for training.

FACILITATOR: Those are interesting different perspectives. How did these feelings evolve over time?

PARTICIPANT_D (Operations Supervisor, 35): For me, the key was the immediate debrief and the way it was handled afterward. When they explained the rationale, showed us statistics about real attacks on similar companies, and emphasized that it was purely educational, my initial anger transformed into appreciation. But I think the communication could have been better from the start.

PARTICIPANT_A: I agree about the communication. Maybe they could have announced that security assessments would be happening without giving specific details about timing or methods. That way we'd know it was coming but wouldn't be able to game the system.

PARTICIPANT_E (Marketing Coordinator, 31): What really changed my perspective was learning about the legal and regulatory requirements for our industry. The compliance officer explained that these simulations are often required by auditors and that our clients expect us to have robust security training. It wasn't just the company being sneaky - it was them meeting their obligations to protect client data.

FACILITATOR: How did peer interactions change after the simulation?

PARTICIPANT_F (Customer Service Rep, 27): There was definitely an initial period of awkwardness. People were comparing who fell for it and who didn't, which created some tension. But as we started having more open discussions about it, that competitive dynamic shifted toward collaborative learning.

PARTICIPANT_D: Exactly. We started talking more openly about security concerns in general. Before the simulation, admitting confusion about an email or asking for help felt embarrassing, like you were admitting incompetence. Now we collaborate more readily on suspicious emails, and it's seen as good judgment rather than weakness.

PARTICIPANT_G (Research Assistant, 26): I noticed people started forwarding examples of real phishing emails they received, which became valuable learning opportunities. We created an informal knowledge-sharing system where interesting attack attempts get discussed and analyzed by the group.

PARTICIPANT_H (Project Coordinator, 42): The simulation also revealed how different departments face different types of threats. Finance gets targeted with fake invoice and payment requests, HR sees resume attachments with malware, and sales receives fake prospect inquiries. Sharing these department-specific threats has been really valuable.

FACILITATOR: What made the training effective or ineffective for your learning?

PARTICIPANT_B: The immediate, detailed feedback was crucial. Getting a real-time explanation of why the email was suspicious, what techniques were used, and how I could have identified it helped reinforce the learning. Without that immediate connection between action and education, it would have just been a trick rather than a teaching moment.

PARTICIPANT_C: The follow-up discussion sessions were equally valuable. Understanding how others analyzed the same email, hearing their thought processes, and learning from their strategies helped me identify blind spots in my own approach.

PARTICIPANT_E: I appreciated that they provided multiple example scenarios after the initial simulation. One test isn't enough to cover the variety of tactics attackers use. Having a series of examples with increasing complexity helped build skills progressively.

PARTICIPANT_F: The group analysis sessions were particularly effective. When we looked at examples as a team, people shared different red flags they noticed, and collectively we could identify things that individuals might miss.

FACILITATOR: Were there aspects of the training that were less effective?

PARTICIPANT_A: I think they underestimated the emotional impact. While they provided technical education, there wasn't much support for processing the feelings of vulnerability and embarrassment that came with falling for the simulation.

PARTICIPANT_G: The timing could have been better communicated. Some people received the simulation during particularly stressful periods, which made them more vulnerable and also more upset about being tested during those times.

PARTICIPANT_H: I would have liked more information about what happens to the data they collected. Do they track individual performance over time? Is it truly anonymous? More transparency about the data use would have helped with trust issues.

FACILITATOR: How has the overall security culture in the organization changed?

PARTICIPANT_D: There's definitely more security awareness in daily conversations. People mention security considerations in meetings, and there's less stigma around being cautious or asking questions about suspicious communications.

PARTICIPANT_B: We've also become more supportive of each other. If someone receives a questionable email, they're more likely to ask colleagues for a second opinion rather than just hoping for the best or feeling embarrassed about not knowing.

PARTICIPANT_C: I've noticed leadership taking security more seriously too. Managers are more willing to delay decisions to verify authenticity, and there's more understanding that security processes might slow things down but are ultimately worth it.
            """,
            'word_count': 985,
            'data_collection_date': datetime.now() - timedelta(days=random.randint(1, 90))
        },
        {
            'participant_id': 'FG_002',
            'data_type': 'focus_group',
            'interview_type': 'Psychological Needs & Motivation',
            'role': '7 participants (mixed roles)',
            'age': 'Mixed ages 28-49',
            'focus_areas': 'autonomy, competence, relatedness, motivation, self_determination, learning_psychology',
            'transcript_text': """
FACILITATOR: Today we're exploring how the phishing simulation affected your basic psychological needs - your sense of autonomy, competence, and connection with others. Let's start with autonomy. How did the experience affect your sense of control and choice?

PARTICIPANT_I (Software Engineer, 32): Initially, it completely undermined my sense of autonomy. I felt like I was being manipulated and tested without my consent, which made me feel powerless and reactive rather than proactive. But as I learned more about the threats we actually face, I began to see the training as giving me more tools to make informed decisions about my digital security.

PARTICIPANT_J (Nurse, 41): The educational framing was really important for me. Once I understood that this was about empowerment rather than surveillance, I felt more in control. The training showed me multiple ways to handle suspicious emails - reporting, verifying through other channels, seeking colleague input - so I had choices rather than just one rigid protocol.

PARTICIPANT_K (Legal Assistant, 29): What helped my sense of autonomy was learning the 'why' behind security practices, not just the 'what.' Understanding how different types of attacks work and what attackers are trying to achieve helped me make more informed decisions rather than just following rules blindly.

FACILITATOR: How did the simulation impact your sense of competence?

PARTICIPANT_L (Laboratory Technician, 36): That was a real rollercoaster for me. Falling for the initial simulation severely damaged my confidence - I felt stupid and technologically incompetent. But the learning process that followed gradually rebuilt my competence. Starting with obvious phishing examples and progressing to more subtle ones helped me develop skills systematically rather than just highlighting my failures.

PARTICIPANT_M (Office Manager, 45): I had a similar experience. The immediate aftermath was devastating for my confidence, but the structured learning that followed was empowering. I realized that recognizing these attacks isn't just about technical knowledge - it requires understanding psychology and social engineering tactics, which made the challenge feel more intellectually interesting rather than just about technical competence.

PARTICIPANT_N (Research Coordinator, 33): For me, competence came from understanding that even security professionals fall for sophisticated attacks sometimes. Learning that this is a skill that requires ongoing development, rather than something you either have or don't have, made the learning feel more achievable and less threatening to my self-image.

PARTICIPANT_O (Administrative Assistant, 52): The group learning component was crucial for building competence. Seeing that even people I consider tech-savvy struggled with some scenarios normalized the difficulty and made me feel less alone in my confusion.

FACILITATOR: How did the social aspects of the training affect your sense of connection and relatedness?

PARTICIPANT_I: The group debriefing sessions created a real sense of shared responsibility and mutual support. We weren't just protecting our individual accounts anymore - we were part of a collective defense system. That sense of working together toward a common goal was motivating and made the effort feel more meaningful.

PARTICIPANT_J: Exactly. It fostered what I'd call a security-conscious culture where helping each other is encouraged and normalized rather than seen as admitting weakness. There's now a sense of camaraderie around security vigilance.

PARTICIPANT_K: The simulation also revealed how much we can learn from each other. Different people noticed different red flags in the same email, and combining our perspectives made everyone more effective. It highlighted the value of collaboration over individual expertise.

FACILITATOR: What motivated you to apply what you learned from the training?

PARTICIPANT_L: Knowing that my vigilance protects not just my own data but potentially prevents broader organizational breaches gave the effort more significance. It's not just personal security anymore - it's contributing to something larger than myself.

PARTICIPANT_M: The practical relevance was hugely motivating. These aren't abstract, theoretical threats - they're real risks we face in our daily work. Every email could potentially be a test of what I learned.

PARTICIPANT_N: For me, the motivation came from transforming a negative experience (falling for the simulation) into something positive and educational. I wanted to prove to myself that I could learn and improve, not just avoid being tricked again.

FACILITATOR: How sustainable is your motivation to maintain these new security practices?

PARTICIPANT_O: The initial high-alert phase lasted several weeks, but it's settled into more sustainable habits. The key was making the new behaviors automatic rather than requiring constant conscious effort.

PARTICIPANT_I: I think the social reinforcement helps with sustainability. When colleagues ask for help with suspicious emails or share their own experiences, it keeps security awareness active in our daily interactions.

PARTICIPANT_J: Having clear, achievable goals helped too. Instead of trying to become a security expert overnight, I focused on developing specific skills like verifying sender authenticity or recognizing urgency manipulation tactics.

FACILITATOR: Did the training address your need for growth and learning?

PARTICIPANT_K: Absolutely. It opened up a whole new area of knowledge that I find genuinely interesting. Understanding how social engineering works, learning about different attack vectors, and staying current with emerging threats has become an ongoing intellectual pursuit rather than just a work requirement.

PARTICIPANT_L: The progressive skill-building approach satisfied my need for mastery. Starting with basic concepts and gradually tackling more sophisticated scenarios gave me a sense of advancement and growing expertise.

PARTICIPANT_M: It also connected to broader digital literacy skills that are valuable beyond just security. Understanding how online manipulation works has made me more thoughtful about all my digital interactions, from social media to online shopping.

FACILITATOR: Any concerns about the psychological impact of heightened vigilance?

PARTICIPANT_N: There was an initial period where I became somewhat paranoid and anxious about all digital communications. But learning to channel that awareness productively rather than letting it become overwhelming anxiety was part of the learning process.

PARTICIPANT_O: The key was developing confidence in my decision-making process rather than just being generally suspicious. Having systematic approaches to evaluate emails gave me tools to manage uncertainty without being paralyzed by it.
            """,
            'word_count': 1048,
            'data_collection_date': datetime.now() - timedelta(days=random.randint(1, 90))
        }
    ]

def generate_short_interviews():
    """Generate short interview transcripts"""
    return [
        {
            'participant_id': 'SHORT_001',
            'data_type': 'short_interview',
            'interview_type': 'Preparedness Assessment',
            'role': 'Database Administrator',
            'age': 39,
            'focus_areas': 'preparedness, self_efficacy, confidence',
            'transcript_text': """
RESEARCHER: How prepared do you feel against phishing attacks now compared to before the simulation?

PARTICIPANT: Much more prepared, but I've learned that preparation isn't just about technical knowledge - it's about mindset and systematic thinking. Before, I was overconfident based on my technical background. The simulation showed me that attackers target psychology, not just technical vulnerabilities. Now I'm more skeptical by default, which feels safer but can be mentally exhausting. I've developed verification habits that are becoming automatic, and I understand the importance of staying updated on new attack techniques.

RESEARCHER: How has your confidence changed specifically?

PARTICIPANT: It's become more realistic and process-based rather than intuition-based. Before, I trusted my gut instincts about emails, but the simulation showed me how those instincts can be manipulated. Now I'm confident in my systematic approach to email evaluation rather than just my immediate impressions. I know when to pause, what questions to ask myself, and when to seek additional verification. This methodical confidence feels more reliable than my previous overconfidence.
            """,
            'word_count': 180,
            'data_collection_date': datetime.now() - timedelta(days=random.randint(1, 90))
        },
        {
            'participant_id': 'SHORT_002',
            'data_type': 'short_interview',
            'interview_type': 'Ethics & Deception',
            'role': 'Communications Manager',
            'age': 43,
            'focus_areas': 'deception_ethics, trust, organizational_relationship',
            'transcript_text': """
RESEARCHER: How did you feel about being deceived during the experiment, and how do you view the ethics of this approach?

PARTICIPANT: I had very mixed feelings about the deception aspect. Intellectually, I understand the necessity - you can't test people's real responses to phishing if they know it's fake. But emotionally, it felt like a violation of trust between employee and employer. The key factor that made it acceptable was the immediate disclosure and comprehensive educational follow-up. If they had just tricked us without explanation or learning opportunity, it would have been purely manipulative. The educational context transformed deception into a valuable learning experience.

RESEARCHER: Would you participate in similar training again?

PARTICIPANT: Absolutely, now that I understand the purpose and approach. The temporary discomfort of being deceived was far outweighed by the lasting value of the learning. I'd rather be deceived in a controlled educational environment than by actual attackers with malicious intent. However, I think organizations need to be very transparent about using these methods and ensure robust ethical oversight of such programs.
            """,
            'word_count': 191,
            'data_collection_date': datetime.now() - timedelta(days=random.randint(1, 90))
        },
        {
            'participant_id': 'SHORT_003',
            'data_type': 'short_interview',
            'interview_type': 'Behavioral Sustainability',
            'role': 'Quality Assurance Manager',
            'age': 37,
            'focus_areas': 'behavioral_change, sustainability, habit_formation',
            'transcript_text': """
RESEARCHER: What specific behaviors have changed since the simulation, and how sustainable are these changes?

PARTICIPANT: Several key behaviors changed. I now verify financial requests through multiple channels, immediately report suspicious emails rather than just deleting them, and I've developed a habit of pausing before clicking any link or attachment. The high-vigilance phase lasted about two weeks, then settled into more sustainable routines. The key was practicing the new behaviors until they became automatic rather than requiring constant conscious effort.

RESEARCHER: What factors helped maintain these behavioral changes?

PARTICIPANT: Having clear protocols helped enormously. Instead of just being told to 'be careful,' I now have specific steps to follow when evaluating emails. The peer reinforcement was also crucial - when colleagues ask for help with suspicious emails or share their own experiences, it keeps security awareness active in our daily interactions. The organization's supportive approach to questions and mistakes made it easier to maintain vigilant behaviors without fear of judgment.
            """,
            'word_count': 168,
            'data_collection_date': datetime.now() - timedelta(days=random.randint(1, 90))
        }
    ]

# Generate all three types and save to separate CSVs
interviews = generate_individual_interviews()
focus_groups = generate_focus_groups()
short_interviews = generate_short_interviews()

# Save to separate CSV files
pd.DataFrame(interviews).to_csv('../data/transcript_individual_interviews.csv', index=False)
pd.DataFrame(focus_groups).to_csv('../data/transcript_focus_groups.csv', index=False)
pd.DataFrame(short_interviews).to_csv('../data/transcript_short_interviews.csv', index=False)