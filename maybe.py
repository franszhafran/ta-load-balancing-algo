def find_maximum_attack(cards, budget):
  # Sort the cards by attack points in descending order
  sorted_cards = sorted(cards, key=lambda x: x['attack']-x['cost'], reverse=True)

  max_attack = 0
  selected_cards = []
  for card in sorted_cards:
    if card['cost'] <= budget:
        selected_cards.append(card)
        budget -= card['cost']
        max_attack += card['attack']

  return selected_cards, max_attack

raw = """100 9997 783 881 813 721 808 721 739 892 790 934 873 882 736 721 871 889 809 808 903 829 848 728 832 915 749 765 708 826 778 836 884 894 769 890 698 778 803 740 931 803 797 832 856 928 764 894 684 835 868 725 810 821 800 840 812 783 874 789 789 800 831 911 779 762 964 751 958 816 838 828 800 877 702 957 739 727 929 946 855 741 810 767 869 856 725 782 865 809 904 778 865 890 676 909 778 798 812 888 847 784 804 845 871 878 758 799 886 836 944 730 782 809 841 860 738 938 998 733 847 921 807 729 917 895 708 958 837 746 802 797 833 727 950 899 863 936 753 816 913 894 854 749 680 755 986 720 922 831 871 854 668 804 836 909 684 768 730 869 790 850 807 835 885 811 884 818 847 799 886 760 827 819 903 727 680 843 761 770 813 811 962 859 716 725 673 787 839 724 793 852 804 829 838 842 722 801 841 854 954 741
"""
rawr = raw.split(" ")
rawr = rawr[2:]

cards = []
card_number = 1
for i in range(len(rawr)):
    if i % 2 == 0:
        cards.append({
            'name': "card{}".format(card_number),
            'attack': int(rawr[i]),
            'cost': int(rawr[i+1]),
        })
        card_number += 1

budget = 9997
print(len(cards))
selected_cards, max_attack = find_maximum_attack(cards, budget)
print(selected_cards, len(selected_cards), max_attack)