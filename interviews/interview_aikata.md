# Interview with the first FHERMA winner Aikata

At FHERMA, we believe that cutting-edge innovation in Fully Homomorphic Encryption (FHE) shouldn't be limited to seasoned cryptographers alone. That’s why we’ve designed our challenges to welcome participants from diverse backgrounds: hardware engineers, software developers, students, and early-career researchers alike.

In this interview series, Elvira Kharisova, co-founder of Fair Math and a member of FHERMA organizing committee, speaks with emerging talents who have excelled in our challenges, showing how curiosity, persistence, and fresh perspectives can lead to real breakthroughs in FHE.

![Screenshot 2025-08-09 at 1.27.36 PM](https://d2lkyury6zu01n.cloudfront.net/images/PXL_20240819_231702407.jpg)


Today, we talk with Aikata, a final-year PhD student whose work in Post-Quantum Cryptography and FHE has already earned her the Critical Infrastructure Award from the Austrian Academy of Sciences. Aikata holds degrees from TU Graz and IIT Bhilai, and she’s the winner of all three initial FHERMA challenges. Her story is proof that with the right mindset, even the most advanced cryptographic tools can become accessible and innovative across disciplines.

**Elvira:** Thank you so much, Aikata, for joining us today. I’m really excited to dive into your journey and experience, especially knowing you’ve contributed so much through FHERMA. But let’s start from the beginning: could you tell us a bit about your background and how you found your way into cryptography?

**Aikata:** I was first introduced to cryptography during my bachelor's at IIT Bhilai, India. Back then, both machine learning and cybersecurity were evolving rapidly, and I took elective courses in both areas. Initially, I was more inclined towards ML. However, a newly joined professor- Prof. Dhiman Saha gave us an introductory course in cryptography, and I found it fascinating— how cryptographic schemes protect our privacy in the background, without us even noticing it. What intrigued me was the brainstorming required to come up with schemes and then analyze their security. I did some work in symmetric cryptography during my bachelor's. Later, I moved to Austria for my master's and PhD and started working on post-quantum cryptography under Prof. Sujoy Sinha Roy's supervision.

**Elvira:** That sounds like a solid foundation. It’s always fascinating how a single course or professor can influence your whole trajectory. So, how did your interest in fully homomorphic encryption start to grow from there?

**Aikata:** As part of my PhD, I started working on hardware acceleration for FHE. When designing an FHE accelerator, you need application benchmarks to show the effectiveness of your hardware design. At that point, I had only just started learning FHE. To get a better understanding, I started reproducing small applications like logistic regression using FHE.

**Elvira:** That brings us to FHERMA. How did you discover the challenges?

**Aikata:** I was already following FHE-related pages and groups, and I came across a post about FHERMA challenges. I only knew about Zama at the time, so this was something new. A colleague of mine also told me about the challenges, and I was working on benchmarking anyway, so I thought, “Why not try it out?” Initially, I just wanted to test my understanding of FHE, but once I got started, it was hard to stop.

**Elvira:** And it truly paid off. You won three of the challenges: Sign Evaluation, Matrix Multiplication, and Logistic Function. Could you tell us more about one of those in particular?

**Aikata:** For the matrix multiplication challenge, I spent quite some time reading papers and trying different techniques. I remember spending sleepless nights just thinking of how to improve the results. Eventually, I managed to come up with a different design that made better use of the SIMD capabilities of FHE. At the time, I didn’t know if it was any good. I was just benchmarking against other submissions. Later, my supervisor asked if it was worth writing a paper about it. I checked the current state of the art and found that my method was still the best. So, we wrote a paper and submitted it to INDOCRYPT, and I presented it there.

**Elvira:**  That’s such a great example of how practical experimentation can lead to real research breakthroughs. Out of the three challenges you worked on, was there one that stood out to you personally?

**Aikata:** Matrix multiplication. I remember staying up the whole night trying to understand how other submissions were performing better than mine. That drove me to explore different techniques and refine my design. The live leaderboard helped a lot in that, it kept me motivated.

**Elvira:** It’s great to hear that the format inspired such determination. That was actually one of our core goals when designing FHERMA—giving participants visibility into others’ progress to create a sense of dynamic, healthy competition. It sounds like that really worked in your case.

**Aikata:** Yes, absolutely. Without seeing the other teams' timings or accuracy, I probably wouldn’t have pushed myself as much. It really motivated me to keep looking for improvements.

**Elvira:** I’m glad to hear that. Speaking of community contribution, you probably know that we publish the winning solutions as open source. What’s your take on that practice?

**Aikata:** I fully support it. Without open-source tools like **OpenFHE,** I wouldn’t have learned how to implement even the basics of FHE. Coming from an engineering background, it wasn’t easy to get started, but those resources were invaluable. Open-source work accelerates learning, reduces duplication, and really helps the field evolve collaboratively.

**Elvira:** That’s something we’re very committed to. Outside of FHE, what areas are you currently exploring in your research?

**Aikata:** I’m exploring zero-knowledge proofs (ZKPs) to combine them with FHE and achieve IND-CCA security. ZKPs are also slow, like FHE, and I’m currently working on making them faster using GPUs. I might later look into custom hardware acceleration for ZKPs too.

**Elvira:** That’s an exciting direction. Is there anything else you'd like to see in future FHERMA challenges?

**Aikata:** One of the biggest difficulties I faced was that the recent challenges had large parameters. I couldn’t run them on my local machines. If you could give access to a cluster, even during development (not just at submission time), that would make things easier.

**Elvira:** That’s very useful feedback. I’ll make sure to pass it on to the organizing team. Before we close, anything you’d like to add? 

**Aikata:** It was a fun experience. I hadn’t had this kind of competitive drive since my undergrad. I’d love to see FHERMA grow into a library of FHE building blocks for applications. It would be great to have blog posts or talks showing how those blocks are used in larger systems.

**Elvira:** If you're interested in that direction, you can read more about our work on **Polycircuit** and our Decentralized FHE Computer in this [article](https://github.com/fairmath/research/blob/main/Decentralized%20FHE%20Computer.pdf) . Thank you again, Aikata—both for your contributions and for taking the time to speak with us. 

---

This interview is part of a series featuring participants of the FHERMA challenges. More stories are on the way — stay tuned!

In the meantime, you can explore the [current challenges](https://fherma.io/challenges) and try your hand at solving them. You’re also welcome to revisit past challenges and even try to beat Aikata’s score!*

*Please note: Past challenges are no longer eligible for prizes, but you can still submit improved solutions to support learning and contribute to the community.