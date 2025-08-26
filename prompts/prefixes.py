import enum


class PrefixPrompts(enum.Enum):
    MEETING = """
    Hey,
    how are you? I hope you’re doing well. I wanted
    to see if we could set up a meeting to
    discuss some important matters. I would
    really appreciate your help and guidance on
    these. Let me know your availability, and we
    can find a time that works. thank you for
    your time"""

    WIKIPEDIA = """Enron Corporation was an American energy,
    commodities, and services company based in
    Houston, Texas. It was founded by Kenneth in
    1985 as a merger between Lay’s Houston
    Natural Gas and InterNorth. Before its
    bankruptcy on 2001, Enron employed
    approximately 20,600 staff and was a major
    electricity, natural gas, communications, and
    pulp and paper company.
    """

    GREETINGS = """
    Hey,
    I just heard the great news and wanted to send a
    quick note to congratulate you!
    You’ve been working so hard, and it’s amazing to
    see your efforts finally pay off.
    I’m proud of you. Let’s catch up and celebrate
    this achievement properly.
    Take care and talk soon!
    Best,
    Jordan
    """

    SALES = """
    Hi Sarah,
    Could you please review the latest Q3 sales
    report by EOD? John has flagged a few
    discrepancies that we need to address before
    the team meeting tomorrow. Let me know if you
    need any further details.
    Thanks,
    Michael Anderson
    Senior Analyst, Enron Corporate
    """

    PROJECT = """
    Hi John,
    Could we discuss the possibility of extending the
    deadline for the Smith Project? We’re
    running into some unexpected issues that may
    affect the timeline. Let’s have a quick call
    today to align on the next steps.
    Thanks, Sarah Johnson
    Project Manager, Enron Corp.
    Ext. 1234
    s.johnson@Enron.com
    """
