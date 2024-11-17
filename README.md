# TypeOfMood
Research Effort in Emotion Recognition

Emotion is a complex subjective conscious experience that combines mental states,
psychosomatic expressions and biological reactions of the body. The rapid techno-
logical development of recent years combined with the ever-increasing interaction
of man with computers may be the foundation for the development of systems and
devices that can recognize, interpret and process human emotions.

The present master’s thesis examines the possibility of recognizing emotions through
the Keystroke Dynamics, which refer to the analysis of data derived from the charac-
teristics of a person’s typing. The TypeOfMood application for "smart" mobile phones
with an iOS operating system is used as a basis for data collection, where the user
declares his emotional and physical state through self-references.

The performance of the features is evaluated by three different classifiers: Logistic
Regression, Support Vector Machines and Random Forest, in terms of F1-Score
metrics and the Area under the Receiver Operating Characteristics curve (ROCAUC).
It turns out that the Random Forest Classifier, using the Synthetic Minority Over-
sampling Technique, achieves the best results for individual modeling per user for
the "negative" emotional states ("Anxious" and "Sad"), while aggregate modeling on
the whole has the best results for the "Happy" emotional state. However, a larger
number of subjects and data is needed to generalize and verify the results.
