/*

Neste serviço capturamos os emails a serem enviados para os usuarios
Aqui implementamos lógicas de retentativas, adicionados um template
ao email, etc.
*/

const { Kafka } = require('kafkajs')

const kafka = new Kafka({
    clientId: 'email-service',
    brokers: ['kafka:29092'],
    retry: {
        maxRetryTime: 30 * 1000,
        retries: 10
    }
})

const consumer = kafka.consumer({
    groupId: 'email-group',
})

const run = async () => {
    // Consuming
    await consumer.connect()
    await consumer.subscribe({ topic: 'email', fromBeginning: false })

    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            console.log({
                partition,
                offset: message.offset,
                value: message.value.toString(),
            })
        },
    })
}

run().catch(console.error)