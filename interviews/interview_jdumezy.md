# Interview with Jules Dumezy

We continue the series of talks with FHERMA challenge winners, and we are talking with Jules Dumezy, the winner of the Lookup Table Challenge in the FHERMA competition.

<p align="center">
  <img src="https://d2lkyury6zu01n.cloudfront.net/images/pp2026.png" width="500"/>
  <br>
</p>


**Elvira**: Hello Jules, thanks for joining, and we're really excited to have this opportunity to learn more about your journey. Could you start by telling us a bit about your background and how you first got into homomorphic encryption?

**Jules:** Thank you for having me. I first heard about homomorphic encryption while finishing my master’s in engineering. I was already drawn to cybersecurity and with a strong foundation in mathematics, cryptography and post-quantum cryptography I quickly became fascinated by FHE that enables real applications to run directly on encrypted data. I started with a project that combined FHE and robotics, then completed an internship in the Netherlands where I explored the theoretical side of FHE in more depth. Around the same time I learned about the FHERMA challenges, which focus on practical implementation; they were very helpful in showing how challenging it can be to optimize real-world FHE applications. That’s a brief summary of my background.

**Elvira:** That’s really interesting, I love how you connected your strong math background with an interest in cybersecurity, and then discovered FHE. It’s fascinating because many people hear about homomorphic encryption in a very academic way, but you experienced both the theoretical and practical sides almost at the same time.  That actually leads to my next question: how did you first hear about FHERMA?

**Jules:** At the time I was new to FHE, essentially a beginner,  so I tried to gather as much information as I could, reading threads on various forums. I came across OpenFHE and its Discourse Forum, where users ask questions, and noticed a post about FHERMA that I hadn’t known about. So I started researching it and soon began taking part in related challenges.

**Elvira:** Exactly, we created FHERMA together with OpenFHE team, and we are collaborating on this project together.  It’s great that you not only discovered FHERMA, but also decided to participate right away. I know you tried several challenges, but the one you really focused on,  and eventually won, was the Lookup Table Challenge. Could you tell us more about your experience? What did you find most difficult or surprising about it, and why did this challenge catch your attention in particular?

**Jules:** At the time I was still quite new to FHE, so I tried several challenges but found them difficult as a beginner. The lookup-table functionality particularly caught my interest, especially its ability to evaluate arbitrary functions. For that reason I decided to focus on this challenge and try to produce a solid solution.

The work itself had two phases. First I had to figure out the mathematical construction; once that was clear, the much longer phase was optimization. That second part turned out to be the most engaging: you design a solid solution, then you see someone submit a better result, so you go back and try to improve yours. That constant pressure to improve was motivating, I kept refining my approach and eventually produced a solution about two to three times better than my initial one.

**Elvira:** That’s fantastic to hear. I can relate to what you said about the competitive element: seeing other people’s solutions, going back, and trying to push your own further. And that was really the idea with FHERMA. Instead of just submitting once and waiting for the results, it’s more dynamic, so you see the progress, you see improvements building on each other. It makes the whole thing a lot more motivating. and it’s so nice to hear it worked that way for you.

As you know we publish the solutions as an open source afterwards. What do you think about it? Do you see the value in publishing solutions open source? What do you think in open source in general?

**Jules:** I’m a big supporter of open source, and I really like what the Polycircuit library brings. In FHE you mainly work with basic operations like addition and multiplication, which are straightforward, but Polycircuit provides highly optimized operators that aren’t obvious to less experienced users. That makes it very valuable: instead of re-inventing low-level components, teams can reuse tailored, efficient building blocks to compose applications for AI or other use cases.

Of course, FHE experts might be able to design better end-to-end solutions for a particular application, but having these small, well-tuned building blocks makes it much easier to construct applications. The fact that it’s open source is important too, because the community can continue improving the implementations over time. Overall, I think it’s a great resource.

**Elvira:** Absolutely, I agree, optimized building blocks are very important, especially for people who are starting out or want to build applications quickly.

I also wanted to ask about another project of yours: you’ve implemented functional bootstrapping for CKKS in a fork of OpenFHE. What motivated you to explore this direction, and what does your implementation add to the existing tools?

**Jules:** It felt like a natural continuation of the lookup-table evaluation work in BFV. Functional bootstrapping for CKKS is relatively new and exciting because it enables arbitrary lookup-table  evaluation in CKKS while also “cleaning” the ciphertext, that is, it reduces the accumulated approximation errors.  I began this project when I started my PhD in October, around the same time two papers on functional bootstrapping appeared. Since there wasn’t, to my knowledge, a public implementation yet, I wanted to prototype one and release it as open source so others could experiment and build on it. The response has been encouraging, people showed real interest because it makes a lot of previously difficult tasks much more feasible. I chose OpenFHE for the implementation because I’m familiar with it and it’s a solid library to build on.

**Elvira:** It’s exciting that you released a proof of concept so early, and that people can already start experimenting with it. And looking ahead, what areas in secure computation are you personally most excited about right now? Where are you focusing your energy?

**Jules:** I think that, regarding functional bootstrapping for CKKS (and CKKS in general), there are many small optimizations and potential extensions that could further boost performance or add capabilities. That’s basically my main research area right now: exploring these new bootstrapping techniques in a field that’s very active and fast-moving, with many recent papers. My goal is to improve CKKS performance enough to enable practical, real-world FHE use essentially pushing toward the breakthrough that would make FHE widely usable.

**Elvira:** That’s very promising, optimization of CKKS and functional bootstrapping seems like one of the big steps toward making FHE practical for real applications.

Maybe to wrap up, what advice would you give to someone just starting out in homomorphic encryption and thinking about joining FHERMA challenges?

**Jules:** Yes, if you have some background in math and computer science, the Fherma Challenges are a great way to get started. That’s how I began with FHE: by trying to use it. You won’t understand everything at first, but it comes with practice. Working on a problem with FHE is an excellent way to learn its capabilities and limitations.  Start small, experiment, and gradually build toward a solid solution for one of Fherma challenges, and peek into the libraries to see how things work under the hood, that really helps deepen your understanding of FHE.

**Elvira:** That’s wonderful advice — to just start experimenting, even without understanding everything at once. That’s so important, because many people get intimidated by FHE, but experimenting and playing around is really the best way to learn.

Thank you so much, Jules, for sharing your story and insights. I’m sure the community will find this conversation really valuable, and we look forward to seeing you in future challenges!

**Jules:** Thank you.

---
If you're interested in FHE or privacy-preserving AI, you’re welcome to explore our current challenges at [https://fherma.io/challenges](https://fherma.io/challenges). You can also revisit past challenges to experiment and try to develop improved solutions.

*Note: Past challenges are no longer eligible for prizes, but submitting improved solutions is encouraged as a way to sharpen your skills and help the community.*