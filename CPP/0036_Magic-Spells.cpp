// 17/10/2026
// Hard
// Inheritance / Magic Spells
// HackerRank: Utilize dynamic_cast for RTTI downcasting and Dynamic Programming for Longest Common Subsequence.

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

class Spell
{
private:
    string scrollName;

public:
    Spell() : scrollName("") {}

    Spell(string name) : scrollName(name) {}

    virtual ~Spell() {}

    string revealScrollName()
    {
        return scrollName;
    }
};

class Fireball : public Spell
{
private:
    int power;

public:
    Fireball(int power) : power(power) {}

    void revealFirepower()
    {
        cout << "Fireball: " << power << endl;
    }
};

class Frostbite : public Spell
{
private:
    int power;

public:
    Frostbite(int power) : power(power) {}

    void revealFrostpower()
    {
        cout << "Frostbite: " << power << endl;
    }
};

class Thunderstorm : public Spell
{
private:
    int power;

public:
    Thunderstorm(int power) : power(power) {}

    void revealThunderpower()
    {
        cout << "Thunderstorm: " << power << endl;
    }
};

class Waterbolt : public Spell
{
private:
    int power;

public:
    Waterbolt(int power) : power(power) {}

    void revealWaterpower()
    {
        cout << "Waterbolt: " << power << endl;
    }
};

class SpellJournal
{
public:
    static string journal;

    static string read()
    {
        return journal;
    }
};

string SpellJournal::journal = "";


void counterspell(Spell* spell)
{
    // Check if the spell is Fireball
    if (Fireball* fireball = dynamic_cast<Fireball*>(spell))
    {
        fireball->revealFirepower();
    }

    // Check if the spell is Frostbite
    else if (Frostbite* frostbite = dynamic_cast<Frostbite*>(spell))
    {
        frostbite->revealFrostpower();
    }

    // Check if the spell is Thunderstorm
    else if (Thunderstorm* thunderstorm = dynamic_cast<Thunderstorm*>(spell))
    {
        thunderstorm->revealThunderpower();
    }

    // Check if the spell is Waterbolt
    else if (Waterbolt* waterbolt = dynamic_cast<Waterbolt*>(spell))
    {
        waterbolt->revealWaterpower();
    }

    // Generic spell
    else
    {
        string spellName = spell->revealScrollName();
        string journal = SpellJournal::read();

        int n = spellName.length();
        int m = journal.length();

        // Longest Common Subsequence
        vector<vector<int>> dp(
            n + 1,
            vector<int>(m + 1, 0)
        );

        for (int i = 1; i <= n; i++)
        {
            for (int j = 1; j <= m; j++)
            {
                if (spellName[i - 1] == journal[j - 1])
                {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                }
                else
                {
                    dp[i][j] = max(
                        dp[i - 1][j],
                        dp[i][j - 1]
                    );
                }
            }
        }

        cout << dp[n][m] << endl;
    }
}


class Wizard
{
public:
    Spell* cast()
    {
        Spell* spell;

        string s;
        cin >> s;

        int power;
        cin >> power;

        if (s == "fire")
        {
            spell = new Fireball(power);
        }
        else if (s == "frost")
        {
            spell = new Frostbite(power);
        }
        else if (s == "water")
        {
            spell = new Waterbolt(power);
        }
        else if (s == "thunder")
        {
            spell = new Thunderstorm(power);
        }
        else
        {
            spell = new Spell(s);

            // For a generic spell, read the journal
            cin >> SpellJournal::journal;
        }

        return spell;
    }
};


int main()
{
    int T;
    cin >> T;

    Wizard Arawn;

    while (T--)
    {
        Spell* spell = Arawn.cast();

        counterspell(spell);

        delete spell;
    }

    return 0;
}