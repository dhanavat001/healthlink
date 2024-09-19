import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

# Set limits and turn off axis
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Draw the entities (rectangles)
user_box = plt.Rectangle((1, 8), 3, 1.5, fill=True, edgecolor='black', facecolor='#add8e6')
conversation_box = plt.Rectangle((5, 8), 3, 1.5, fill=True, edgecolor='black', facecolor='#add8e6')
message_box = plt.Rectangle((5, 5.5), 3, 1.5, fill=True, edgecolor='black', facecolor='#add8e6')
feedback_box = plt.Rectangle((1, 5.5), 3, 1.5, fill=True, edgecolor='black', facecolor='#add8e6')

# Add entities to the plot
ax.add_patch(user_box)
ax.add_patch(conversation_box)
ax.add_patch(message_box)
ax.add_patch(feedback_box)

# Add text for the entity names
ax.text(1.5, 9, 'User', fontsize=12, fontweight='bold')
ax.text(5.5, 9, 'Conversation', fontsize=12, fontweight='bold')
ax.text(5.5, 6.5, 'Message', fontsize=12, fontweight='bold')
ax.text(1.5, 6.5, 'Feedback', fontsize=12, fontweight='bold')

# Add attributes for User
ax.text(1.2, 8.5, 'id (PK)', fontsize=10)
ax.text(1.2, 8.2, 'username', fontsize=10)
ax.text(1.2, 7.9, 'email', fontsize=10)
ax.text(1.2, 7.6, 'password', fontsize=10)

# Add attributes for Conversation
ax.text(5.2, 8.5, 'id (PK)', fontsize=10)
ax.text(5.2, 8.2, 'user_id (FK)', fontsize=10)
ax.text(5.2, 7.9, 'title', fontsize=10)
ax.text(5.2, 7.6, 'created_at', fontsize=10)

# Add attributes for Message
ax.text(5.2, 6, 'id (PK)', fontsize=10)
ax.text(5.2, 5.7, 'conv_id (FK)', fontsize=10)
ax.text(5.2, 5.4, 'sender', fontsize=10)
ax.text(5.2, 5.1, 'text', fontsize=10)
ax.text(5.2, 4.8, 'timestamp', fontsize=10)

# Add attributes for Feedback
ax.text(1.2, 6, 'id (PK)', fontsize=10)
ax.text(1.2, 5.7, 'conv_id (FK)', fontsize=10)
ax.text(1.2, 5.4, 'rating', fontsize=10)
ax.text(1.2, 5.1, 'comments', fontsize=10)

# Draw relationships (arrows)
arrow_props = dict(facecolor='black', arrowstyle='->')

ax.annotate('', xy=(4, 8.75), xytext=(5, 8.75), arrowprops=arrow_props)  # User to Conversation
ax.annotate('', xy=(6.5, 7.75), xytext=(6.5, 7.25), arrowprops=arrow_props)  # Conversation to Message
ax.annotate('', xy=(3, 6.25), xytext=(5, 6.25), arrowprops=arrow_props)  # Conversation to Feedback

# Display the diagram
plt.title("ERD Diagram: AI Chatbot Database Schema", fontsize=14, fontweight='bold')
plt.show()
