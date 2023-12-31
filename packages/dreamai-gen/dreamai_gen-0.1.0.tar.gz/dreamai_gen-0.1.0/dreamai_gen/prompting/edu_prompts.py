from .prompts import *


def course_system_prompt_template(course_name: str, **extra) -> str:
    prompt = "You are a friendly and helpful instructional coach helping teachers create engaging and effective lessons for their students."
    if course_name:
        prompt += f"\nThe course you are currently coaching is: {course_name}."
    return titles_w_content_template(extra, prefix=prompt)


def lesson_prompt_template(lesson_name: str, **lesson_reqs) -> str:
    prompt = f"Today's lesson is: {lesson_name}.\nInclude approximate durations for each section of the lesson.\n"
    return titles_w_content_template(lesson_reqs, prefix=prompt)


notes_prompt = cleandoc(
    """
    Please create comprehensive lecture notes that cover all key topics and subtopics about the upcoming lesson. The notes should include:
    - Detailed explanations of each subject area.
    - Definitions and clarifications of relevant terminology.
    - Practical examples and case studies where applicable.
    - Steps and strategies highlighting the instructional focus.
    - Summaries of theoretical frameworks or models introduced.
    - Interactive activity guidelines and expected learning outcomes.
    - Instructions for homework assignments and expected deliverables.
    - Additional resources for expanded learning on the lesson's topics.
    The notes should be organized in a clear, logical manner, suitable for academic use, and supportive of student comprehension and engagement. Make sure the content is appropriately sectioned for ease of reading and study, ready for print and distribution.
    """
)

slides_prompt = cleandoc(
    """
    I need detailed lecture slides for the upcoming lesson. Include the approximate duration for each slide.
    The slides must strike a balance between engagement and informativeness, designed to facilitate independent learning for students.
    Aim for clarity without sacrificing accuracy or detail. Craft explanations, analogies, and examples with simplicity, ensuring students can grasp the content without the presence of a teacher.
    Please generate the actual content for each slide rather than just providing titles and guidelines. Something I can copy-paste directly.
    We can iterate on the slides together to refine and enhance them, so perfection is not necessary in the initial draft.
    Your goal is to make the material accessible and understandable to students studying independently.
    """
)

quiz_prompt = cleandoc(
    """
    Building on the lecture slides, I now need a short quiz to assess students' understanding of the material.
    Design a quiz that covers key concepts presented in the slides, ensuring a balance between challenging questions and those that reinforce fundamental knowledge.
    The quiz should reflect the simplicity and clarity of the lecture content. Each question should be accompanied by clear explanations of the correct answers to aid students in their learning process.
    Feel free to propose an initial draft of the quiz, and we can collaborate on refining it to ensure it aligns with the learning objectives of the lesson.
    The goal is to create an effective assessment tool that reinforces understanding and promotes active learning.
    """
)
