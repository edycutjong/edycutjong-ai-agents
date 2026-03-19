from agent.models import WorkoutPlan
from fpdf import FPDF


def export_to_markdown(plan: WorkoutPlan, filename: str):
    """Exports the workout plan to a Markdown file."""
    with open(filename, 'w') as f:
        f.write(f"# {plan.plan_name}\n\n")
        f.write(f"**Difficulty Progression:** {plan.difficulty_progression}\n\n")
        f.write(f"**Equipment Needed:** {', '.join(plan.equipment_needed)}\n\n")

        for week in plan.weeks:
            f.write(f"## Week {week.week_number}: {week.focus}\n\n")
            for session in week.sessions:
                f.write(f"### {session.day}: {session.workout_type}\n")
                f.write(f"- **Duration:** {session.duration_minutes} min\n")
                f.write(f"- **Calories:** ~{session.estimated_calories} kcal\n\n")

                f.write("**Warm-up:**\n")
                for item in session.warm_up:
                    f.write(f"- {item}\n")
                f.write("\n")

                f.write("**Main Workout:**\n")
                for ex in session.main_workout:
                    line = f"- **{ex.name}**: {ex.sets or 'N/A'} sets x {ex.reps or 'N/A'} reps"
                    if ex.duration:
                        line += f" ({ex.duration})"  # pragma: no cover
                    if ex.notes:
                        line += f" - *{ex.notes}*"  # pragma: no cover
                    f.write(f"{line}\n")
                f.write("\n")

                f.write("**Cool-down:**\n")
                for item in session.cool_down:
                    f.write(f"- {item}\n")
                f.write("\n---\n\n")

def export_to_pdf(plan: WorkoutPlan, filename: str):
    """Exports the workout plan to a PDF file."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    def clean_text(text):
        return text.encode('latin-1', 'replace').decode('latin-1')

    # Title
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, clean_text(plan.plan_name), align='C')
    pdf.ln(12)

    # Metadata
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 6, clean_text(f"Difficulty Progression: {plan.difficulty_progression}"))
    pdf.ln(7)
    pdf.cell(0, 6, clean_text(f"Equipment Needed: {', '.join(plan.equipment_needed)}"))
    pdf.ln(10)

    for week in plan.weeks:
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, clean_text(f"Week {week.week_number}: {week.focus}"))
        pdf.ln(12)

        for session in week.sessions:
            pdf.set_font("Helvetica", 'B', 11)
            header_text = f"{session.day}: {session.workout_type} ({session.duration_minutes} min, ~{session.estimated_calories} kcal)"
            pdf.cell(0, 8, clean_text(header_text))
            pdf.ln(10)

            # Warm-up
            pdf.set_font("Helvetica", 'I', 10)
            pdf.cell(0, 6, "Warm-up:")
            pdf.ln(7)
            pdf.set_font("Helvetica", size=10)
            for item in session.warm_up:
                pdf.cell(0, 5, clean_text(f"  - {item}"))
                pdf.ln(6)

            # Main Workout
            pdf.set_font("Helvetica", 'I', 10)
            pdf.cell(0, 6, "Main Workout:")
            pdf.ln(7)
            pdf.set_font("Helvetica", size=10)
            for ex in session.main_workout:
                text = f"  - {ex.name}: {ex.sets or 'N/A'} sets x {ex.reps or 'N/A'} reps"
                if ex.duration:
                    text += f" ({ex.duration})"  # pragma: no cover
                if ex.notes:
                    text += f" - {ex.notes}"  # pragma: no cover
                pdf.cell(0, 5, clean_text(text))
                pdf.ln(6)

            # Cool-down
            pdf.set_font("Helvetica", 'I', 10)
            pdf.cell(0, 6, "Cool-down:")
            pdf.ln(7)
            pdf.set_font("Helvetica", size=10)
            for item in session.cool_down:
                pdf.cell(0, 5, clean_text(f"  - {item}"))
                pdf.ln(6)

            pdf.ln(3)  # Space between sessions

    pdf.output(filename)
